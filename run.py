""" Love sandwhiches walkthrough project """

# imports
import gspread
from google.oauth2.service_account import Credentials

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
sales = SHEET.worksheet('sales')

# getting all the values from the sales worksheet
data = sales.get_all_values()


# getting the sales data
def get_sales_data():
    """
    Get sales figures input from the user. Calls validate_data()
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60")

    data_str = input("Enter you data here: ")

    # splitting at the commas
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the Try, converts all string values into integers.
    Raises ValueError if string cannot be converted into int,
    or if there arent exactly 6 values.
    Called by get_sales_data()
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()
