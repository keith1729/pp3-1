
import gspread
from google.oauth2.service_account import Credentials
import sys
from colorama import Fore
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the_bank')

accounts_worksheet = SHEET.worksheet('accounts')

def current_time_date():
    local_tz = pytz.timezone('Europe/Dublin')
    current_tz = datetime.now(local_tz).strftime('(%H:%M:%S, %d-%m-%Y)')
    return current_tz

def characters(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def clear_screen():
    os.system('clear')


def welcome():
    while True:
        try:
            clear_screen()
            characters(f'''{Fore.YELLOW}{logo}''')
            time.sleep(2)
            characters(f'''{Fore.WHITE}
    Welcome to The Bank! {current_time_date()}

    Please choose an option:

    [1] Login
    [2] Create New Account
            ''')
            
            login_option = int(input('\n>> '))
            
            if login_option == 1:
                login()
                break
            elif login_option == 2:
                create_new_acc()
                break
            else:
                print("\nPlease choose a valid option (1 or 2)\n")
                time.sleep(4)
                welcome()
        except ValueError:
            print('\nInvalid input. Please enter a number (1 or 2)\n')
            time.sleep(4)
            welcome()

welcome()
