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

print(data)