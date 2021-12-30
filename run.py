""" Love sandwhiches walkthrough project """

# imports
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# list of APIs the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# other vars which shouldnt be changed
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# gspread client
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# accessing the google sheet
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# accessing the worksheet in the google sheet
# sales = SHEET.worksheet('sales')

# getting all the values from the sales worksheet
# data = sales.get_all_values()


# getting the sales data
def get_sales_data():
    """
    Get sales figures input from the user.
    Run while loop to collect valid string of data from user
    via the terminal, which must be a string of 6 numbers separated
    by commas.
    The loop continues until correct data is entered.
    Calls validate_data()
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter you data here: ")

        # splitting at the commas
        sales_data = data_str.split(",")

        # if data is valid the loop is exited
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the Try, converts all string values into integers.
    Raises ValueError if string cannot be converted into int,
    or if there arent exactly 6 values.
    Called by get_sales_data()
    """
    try:
        # trying to convert the values to ints
        [int(value) for value in values]
        # specific error message for if length is wrong
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    # where e is the error message
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, sheet):
    """
    Update sales/surplus/stock worksheet, add new row with the list data
    provided.
    """
    print(f"Updating {sheet} worksheet... \n")
    # accessing the worksheet with the worksheet method and gspread
    worksheet = SHEET.worksheet(sheet)
    # adding the new row of data
    worksheet.append_row(data)
    print(f"{sheet} worksheet updated. \n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock data to calculate the surplus for each item.

    The surplus is defined as the sales figure subtracted from the stock:
    -positive surplus indicates waste
    -negative surplus indicates extra made when stock ran out
    """
    print("Calculating surplus data ... \n")
    # retriving all the stock data values
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting the last
    5 entries for each sandwich and returns the data in a list of lists.
    """
    sales = SHEET.worksheet('sales')
    # accessing each column (the sandwich types)
    columns = []
    for i in range(1, 7):
        column = sales.col_values(i)
        # appending only the last 5 values of each column as lists
        columns.append(column[-5:])
    return columns


def main():
    """
    Running all program functions in order
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    # update_sales_worksheet(sales_data)
    update_worksheet(sales_data, 'sales')
    row_surplus_data = calculate_surplus_data(sales_data)
    # update_surplus_worksheet(row_surplus_data)
    update_worksheet(row_surplus_data, 'surplus')


print("Welcome to Love Sandwiches Data Automation")
# main()
sales_columns = get_last_5_entries_sales()
