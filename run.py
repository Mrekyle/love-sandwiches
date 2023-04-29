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
    while True:
        print('Please enter the sales data from the latest Market day.')
        print('Data should be six numbers and seperated by commas')
        print('Example: 20, 3, 54, 19, 43, 21\n')

        data_str = input('Please enter your data here: ')    
        sales_data = data_str.split(',')  # Removes the commas from the string and creates individual items
        
        if validate_data(sales_data):  # Calls the valiadata data function to validate the inputted data
            print('Data is valid!')
            break
        # If statement meand the while loop will continue to run until the validate_data returns true

    return sales_data

def validate_data(values): 
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        # Above converts the string into integers. Allowing us to check if it is a value we can accept
        if len(values) != 6:  # If the length of the string is less than 6 it will cause the error
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:  # Setting the value error as the variable. To be able to print out in the statement
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Updates the sales worksheet, adds new row with the list data received 
    """
    print('Currently updating the sales worksheet....\n')
    sales_worksheet = SHEET.worksheet('sales')  # Accessing the worksheet tab. Not the document like above
    sales_worksheet.append_row(data)  # Adds a new row of data to the sales worksheet 
    print('Sales worksheet updated successfully.\n')

def calculate_surplus_stock(sales_row):
    """
    Calculates the surplus sandwich stock at the end 
    of the market day
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    print(stock_row)



def main():  # Common practice to add all function calls inside a main function, So only calling one function 
    """
    Runs all main program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_stock(sales_data)


print('Welcome to Love Sandwiches Data automation service.\n')
main()