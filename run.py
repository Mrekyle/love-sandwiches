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
        print('Data should be six numbers and separated by commas')
        print('Example: 20, 3, 54, 19, 43, 21\n')

        data_str = input('Please enter your data here:\n')    
        sales_data = data_str.split(',')  # Removes the commas from the string and creates individual items
        
        if validate_data(sales_data):  # Calls the validate data function to validate the inputted data
            print('Data is valid!')
            break
        # If statement means the while loop will continue to run until the validate_data returns true

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

# def update_sales_worksheet(data):
#     """
#     Updates the sales worksheet, adds new row with the list data received 
#     """
#     print('Currently updating the sales worksheet....\n')
#     sales_worksheet = SHEET.worksheet('sales')  # Accessing the worksheet tab. Not the document like above
#     sales_worksheet.append_row(data)  # Adds a new row of data to the sales worksheet 
#     print('Sales worksheet updated successfully.\n')

# def update_surplus_worksheet(data):
#     """
#     Updates the surplus stock worksheet calculated by the sales data  
#     """
#     print('\nCurrently updating the surplus stock worksheet...\n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print('Surplus data worksheet updated successfully.\n')


def update_worksheet(data, worksheet):  # Refactored update worksheet function to remove repeated code
    """
    Updates the worksheet based on the worksheet required to be updated
    """
    print(f"Currently updating the {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet was updated successfully.\n")

def calculate_surplus_stock(sales_row):
    """
    Calculates the surplus sandwich stock at the end 
    of the market day
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()  # Gets all the values from the stock sheet
    stock_row = stock[-1]  # Gets the last row of the values in the stock worksheet

    surplus_data = []
    for stock, sales, in zip(stock_row, sales_row):  # zip() allows us to iterate through multiple lists at the same time
        surplus = int(stock) - sales  # Subtracting the two figures from each other
        surplus_data.append(surplus)  # Appending the list to the surplus data list. Ready to add to the worksheet

    return surplus_data

def get_last_5_entries_sales():
    """
    Gets the last 5 sales data entries.
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculates the average stock from the sales of the last 5 market days. 
    Adding 10%
    """
    print('Calculating the Average stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]  # Converting the string into integers 
        average = sum(int_column) / len(int_column)  # Calculates the average of the last 5 market days data
        stock_num = average * 1.1  # Adds 10% to the total number inside the average variable
        new_stock_data.append(round(stock_num))  # Appends the data to the new list whilst also rounding the data to the nearest whole number

    return new_stock_data 

def main():  # Common practice to add all function calls inside a main function, So only calling one function 
    """
    Runs all main program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_stock(sales_data)
    update_worksheet(new_surplus_data, "surplus")  # Calls the update function passing which worksheet to be updated.
    sales_column = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, "stock")
    #  Allowing us to actively change the string displayed. 


print('Welcome to Love Sandwiches Data automation service.\n')
main()