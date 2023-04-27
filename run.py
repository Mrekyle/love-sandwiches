"""
python3 run.py - Will allow the app to run in the terminal
"""

import gspread  # Importing an entire library
from google.oauth2.service_account import Credentials
# Importing one function from the library

SCOPE = [  # Telling the application what API's it will have access to
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
# Reads the credentials allowing access to the google API
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# Accesses the google docs spreadsheet with the open method

sales = SHEET.worksheet('sales')
# Using the SHEET method to read the sales sheet data inside of the document
data = sales.get_all_values()
# Getting all the data inside of the sales file.


print(data)
