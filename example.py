from pygdoc import GoogleDocManager
import pandas as pd
import os
import json

os.environ['GOOGLE_SERVICE_ACCOUNT_FILE'] = 'service_account.json'
service_account_file = os.environ['GOOGLE_SERVICE_ACCOUNT_FILE']

# Load the service account info from a JSON file
with open(service_account_file, 'r') as f:
    service_account_info = json.load(f)

doc_manager = GoogleDocManager(service_account_info=service_account_info)

doc_manager.get_current_document()