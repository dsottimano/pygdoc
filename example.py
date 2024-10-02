from pygdoc import GoogleDocManager
import pandas as pd
import os
os.environ['GOOGLE_SERVICE_ACCOUNT_FILE'] = 'service_account.json'
service_account_file = os.environ['GOOGLE_SERVICE_ACCOUNT_FILE']



doc_manager = GoogleDocManager(service_account_info=service_account_file)

doc_id = doc_manager.create_google_doc("My New Document", force=True)
print(doc_id)
# # Share the document
doc_manager.share_google_doc(doc_id, "dsottimano@gmail.com")

# Insert a heading
doc_manager.insert_heading_to_doc("My Heading", heading_level=1)

# Insert a paragraph
doc_manager.insert_paragraphs_to_doc("This is a paragraph.")

# Insert an image
doc_manager.insert_image_to_doc("https://example.com/image.png")

# Create a table from a DataFrame
df = pd.DataFrame({"Column1": [1, 2], "Column2": [3, 4]})
doc_manager.create_table_from_df(df)

# Replace string with page break
doc_manager.replace_string_with_page_break("<pagebreak>")

# Insert a page break
doc_manager.insert_page_break()