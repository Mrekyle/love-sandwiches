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

# sales = SHEET.worksheet('sales')
# # Using the SHEET method to read the sales sheet data inside of the document
# data = sales.get_all_values()
# # Getting all the data inside of the sales file.

def get_sales_data():
    """
    Gets sales data from the user
    """
    print('Please enter the sales data from the latest Market day.')
    print('Data should be six numbers and seperated by commas')
    print('Example: 20, 3, 54, 19, 43, 21\n')

    data_str = input('Please enter your data here: ')    
    sales_data = data_str.split(',')
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()