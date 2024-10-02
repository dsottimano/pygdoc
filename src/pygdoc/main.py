import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from gdoctableapppy import gdoctableapp
import time
import random

class GoogleDocManager:
    def __init__(self, service_account_file, delay=2, max_retries=5):
        """
        Initialize the GoogleDocManager with the given service account file.

        Args:
            service_account_file (str): Path to the service account JSON file.
            delay (int): Initial delay between retries in seconds (default is 2).
            max_retries (int): Maximum number of retries (default is 5).
        """
        self.scopes = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
        self.creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=self.scopes)
        self.service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.document_id = None
        self.delay = delay
        self.max_retries = max_retries

    def get_last_index(self):
        """
        Get the last index in the Google Doc.

        Returns:
            int: The last index in the document.
        """
        document = self.retry_with_exponential_backoff(self.service.documents().get, documentId=self.document_id)
        body_content = document.get('body', {}).get('content', [])
        if not body_content:
            return 1
        last_element = body_content[-1]
        return last_element.get('endIndex', 1) - 1

    def create_google_doc(self, title, force=False):
        """
        Create a new Google Doc with the given title.

        Args:
            title (str): The title of the new document.
            force (bool): If True, create a new document even if one already exists.

        Returns:
            str: The document ID of the created document.
        """
        if self.document_id and not force:
            print(f'Document already exists with ID: {self.document_id}')
        else:
            body = {'title': title}
            doc = self.retry_with_exponential_backoff(self.service.documents().create, body=body)
            self.document_id = doc.get('documentId')
        document_url = f"https://docs.google.com/document/d/{self.document_id}/edit"
        print(document_url)
        return self.document_id

    def share_google_doc(self, file_id, email, role='writer'):
        """
        Share the Google Doc with a specified email.

        Args:
            file_id (str): The ID of the file to share.
            email (str): The email address to share the document with.
            role (str): The role to assign to the email (default is 'writer').
        """
        permission = {'type': 'user', 'role': role, 'emailAddress': email}
        self.retry_with_exponential_backoff(self.drive_service.permissions().create, fileId=file_id, body=permission)

    def insert_text_to_doc(self, text, index):
        """
        Insert text into the Google Doc at the specified index.

        Args:
            text (str): The text to insert.
            index (int): The index at which to insert the text.
        """
        requests = [{'insertText': {'location': {'index': index}, 'text': text}}]
        self.retry_with_exponential_backoff(self.service.documents().batchUpdate, documentId=self.document_id, body={'requests': requests})

    def insert_spacer_to_doc(self):
        """
        Insert a spacer (two newlines) into the Google Doc.
        """
        index = self.get_last_index()
        self.insert_text_to_doc("\n\n", index)

    def insert_heading_to_doc(self, heading_text, heading_level=1):
        """
        Insert a heading into the Google Doc.

        Args:
            heading_text (str): The text of the heading.
            heading_level (int): The level of the heading (default is 1).
        """
        index = self.get_last_index()
        heading_style = f'HEADING_{heading_level}'
        requests = [
            {'insertText': {'location': {'index': index}, 'text': heading_text + "\n"}},
            {'updateParagraphStyle': {'range': {'startIndex': index, 'endIndex': index + len(heading_text)}, 'paragraphStyle': {'namedStyleType': heading_style}, 'fields': 'namedStyleType'}}
        ]
        self.retry_with_exponential_backoff(self.service.documents().batchUpdate, documentId=self.document_id, body={'requests': requests})

    def insert_image_to_doc(self, image_url, width=300, height=300):
        """
        Insert an image into the Google Doc.

        Args:
            image_url (str): The URL of the image.
            width (int): The width of the image in points (default is 300).
            height (int): The height of the image in points (default is 300).
        """
        index = self.get_last_index()
        requests = [{'insertInlineImage': {'location': {'index': index}, 'uri': image_url, 'objectSize': {'height': {'magnitude': height, 'unit': 'PT'}, 'width': {'magnitude': width, 'unit': 'PT'}}}}]
        self.retry_with_exponential_backoff(self.service.documents().batchUpdate, documentId=self.document_id, body={'requests': requests})

    def retry_with_exponential_backoff(self, func, *args):
        """
        Retry a function with exponential backoff.

        Args:
            func (callable): The function to retry.
            *args: Arguments to pass to the function.

        Returns:
            Any: The return value of the function, if successful.

        Raises:
            Exception: If the function fails after the maximum number of retries.
        """
        attempt = 0
        current_delay = self.delay
        while attempt < self.max_retries:
            try:
                return func(*args).execute()
            except Exception as e:
                attempt += 1
                print(f"Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep_time = current_delay + random.uniform(0, 1)
                    print(f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                    current_delay *= 2
                else:
                    print("Max retries reached.")
                    raise e

    def insert_paragraphs_to_doc(self, paragraphs):
        """
        Insert multiple paragraphs into the Google Doc.

        Args:
            paragraphs (list or str): The paragraphs to insert.
        """
        if isinstance(paragraphs, str):
            paragraphs = [paragraphs]
        for paragraph in paragraphs:
            self.retry_with_exponential_backoff(self.insert_text_to_doc, paragraph + "\n", self.get_last_index())
            time.sleep(self.delay)

    def create_table_from_df(self, df):
        """
        Create a table in the Google Doc from a pandas DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to convert to a table.
        """
        df = df.astype(str)
        df.columns = df.columns.astype(str)
        values = [df.columns.tolist()] + df.values.tolist()
        resource = {"service_account": self.creds, "documentId": self.document_id, "rows": len(values), "columns": len(df.columns), "append": True, "values": values}
        self.retry_with_exponential_backoff(gdoctableapp.CreateTable, resource)

    def replace_string_with_page_break(self, target_string='<pagebreak>'):
        """
        Replace occurrences of a target string with a page break in the Google Doc.

        Args:
            target_string (str): The string to replace with a page break (default is '<pagebreak>').

        Returns:
            dict: The response from the batchUpdate request.
        """
        document = self.retry_with_exponential_backoff(self.service.documents().get, documentId=self.document_id)
        content = document.get('body', {}).get('content', [])
        requests = []
        for element in content:
            if 'paragraph' in element:
                for paragraph_element in element['paragraph']['elements']:
                    text_run = paragraph_element.get('textRun', {})
                    text_content = text_run.get('content', '')
                    if target_string in text_content:
                        start_index = paragraph_element['startIndex']
                        requests.append({'replaceAllText': {'containsText': {'text': target_string, 'matchCase': True}, 'replaceText': ''}})
                        requests.append({'insertPageBreak': {'location': {'index': start_index}}})
        if not requests:
            return 'No occurrences of the target string found.'
        return self.retry_with_exponential_backoff(self.service.documents().batchUpdate, documentId=self.document_id, body={'requests': requests})

    def insert_page_break(self):
        """
        Insert a page break into the Google Doc.
        """
        index = self.get_last_index()
        requests = [{'insertPageBreak': {'location': {'index': index}}}]
        self.retry_with_exponential_backoff(self.service.documents().batchUpdate, documentId=self.document_id, body={'requests': requests})