# Pygdoc

Pygdoc is a Python class that provides a convenient interface for managing Google Docs. It allows you to create, share, and manipulate Google Docs using the Google Docs API and Google Drive API.

## Features

- Create a new Google Doc
- Share a Google Doc with specified email addresses
- Insert text, headings, images, and page breaks into a Google Doc
- Insert multiple paragraphs into a Google Doc
- Create a table in a Google Doc from a pandas DataFrame
- Replace occurrences of a target string with a page break

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Initialization

To use the `GoogleDocManager`, you need to initialize it with your service account file:

```python
from pygdoc.main import GoogleDocManager

service_account_file = 'path/to/your/service_account.json'
doc_manager = GoogleDocManager(service_account_file)
```

### Creating a New Google Doc

To create a new Google Doc, use the `create_document` method:

```python
doc_id = doc_manager.create_document('Document Title')
print(f'Document created with ID: {doc_id}')
```

### Sharing a Google Doc

To share a Google Doc with specified email addresses, use the `share_document` method:

```python
doc_manager.share_document(doc_id, ['email1@example.com', 'email2@example.com'])
print('Document shared successfully.')
```

### Inserting Text and Headings

To insert text or headings into a Google Doc, use the `insert_text` method:

```python
doc_manager.insert_text(doc_id, 'This is a heading', heading=True)
doc_manager.insert_text(doc_id, 'This is a paragraph.')
```

### Inserting Images

To insert an image into a Google Doc, use the `insert_image` method:

```python
image_url = 'https://example.com/image.png'
doc_manager.insert_image(doc_id, image_url)
```

### Inserting Page Breaks

To insert a page break into a Google Doc, use the `insert_page_break` method:

```python
doc_manager.insert_page_break(doc_id)
```

### Creating a Table from a pandas DataFrame

To create a table in a Google Doc from a pandas DataFrame, use the `insert_table_from_dataframe` method:

```python
import pandas as pd

data = {'Column1': [1, 2], 'Column2': [3, 4]}
df = pd.DataFrame(data)
doc_manager.insert_table_from_dataframe(doc_id, df)
```

### Replacing Text with Page Breaks

To replace occurrences of a target string with a page break, use the `replace_text_with_page_break` method:

```python
doc_manager.replace_text_with_page_break(doc_id, 'target_string')
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [yourname@example.com](mailto:yourname@example.com).