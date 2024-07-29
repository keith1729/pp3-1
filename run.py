
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

logo = '''
 /$$$$$$$$ /$$                       /$$$$$$$                      /$$      
|__  $$__/| $$                      | $$__  $$                    | $$      
   | $$   | $$$$$$$   /$$$$$$       | $$  \\ $$  /$$$$$$  /$$$$$$$ | $$   /$$
   | $$   | $$__  $$ /$$__  $$      | $$$$$$$  |____  $$| $$__  $$| $$  /$$/
   | $$   | $$  \\ $$| $$$$$$$$      | $$__  $$  /$$$$$$$| $$  \\ $$| $$$$$$/ 
   | $$   | $$  | $$| $$_____/      | $$  \\ $$ /$$__  $$| $$  | $$| $$_  $$ 
   | $$   | $$  | $$|  $$$$$$$      | $$$$$$$/|  $$$$$$$| $$  | $$| $$ \\  $$
   |__/   |__/  |__/ \\_______/      |_______/  \\_______/|__/  |__/|__/  \\__/
'''

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


class BankAccount:

    def __init__(self, username, account_number, pin, balance):
        self.username = username
        self.account_number = account_number
        self.pin = pin
        self.balance = float(balance)
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return self.balance
        else:
            raise ValueError('Deposit amount cannot be a negative or zero value!')

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return self.balance
        else:
            raise ValueError('Withdrawal amount cannot be a negative value or above your balance!')


def create_new_acc():

    while True:
        try:
            clear_screen()
            time.sleep(2)
            print(f'''{Fore.YELLOW}{logo}''')
            time.sleep(2)
            characters(f'''{Fore.WHITE}
    To create a new account please enter a Username:
            ''')

            username = input('\n>> ')

            # Validate username (you can add more checks here)
            if username.strip():  # Check if not empty
                break
            else:
                print('\nYou cannot have an empty Username!\n')
                time.sleep(4)
                create_new_acc()
        except ValueError:
            print('\nInput a valid Username!\n')
            time.sleep(4)
            create_new_acc()

    time.sleep(3)
    characters(f'''
    Generating new Account Number and new Pin for {username}...
    ''')

    account_number = 'AC-' + str(random.randint(1000000, 9999999))
    pin = str(random.randint(1000, 9999))

    balance = 0

    user_account = BankAccount(username = username, account_number = account_number, pin = pin, balance = balance)
    time.sleep(6)
    characters(f'''
    Username: {user_account.username}
    Account Number: {user_account.account_number}
    Pin: {user_account.pin}
    Balance: {user_account.balance}
    ''')

    accounts_worksheet = SHEET.worksheet('accounts')
    accounts_worksheet.append_row([user_account.username, user_account.account_number, user_account.pin, user_account.balance])

    proceed(user_account)
    time.sleep(8)
    login()


def login():

    while True:
        try:
            clear_screen()
            time.sleep(2)
            print(f'''{Fore.YELLOW}{logo}''')
            time.sleep(2)
            characters(f'''{Fore.WHITE}
    Please login with Username and Pin!
            ''')
            username_entered = input('\n    Enter Username: ')
            time.sleep(1)
            pin_entered = input('\n    Enter Pin: ')


            username_entered_cell = accounts_worksheet.find(username_entered)
            username_entered_row = username_entered_cell.row

            username_entered_row_username = accounts_worksheet.cell(username_entered_row, 1).value
            username_entered_row_account_number = accounts_worksheet.cell(username_entered_row, 2).value
            username_entered_row_pin = accounts_worksheet.cell(username_entered_row, 3).value
            username_entered_row_balance = accounts_worksheet.cell(username_entered_row, 4).value

            time.sleep(1)
            characters('''
    Validating Username and Pin...
            ''')
            if username_entered == username_entered_row_username and pin_entered == username_entered_row_pin:
                user_account = BankAccount(username = username_entered_row_username, account_number = username_entered_row_account_number, pin = username_entered_row_pin, balance = username_entered_row_balance)
                time.sleep(6)
                characters('''
    Login Successful!
                ''')
                time.sleep(4)
                break           
            else:
                print('\n    Cannot login! Try again...\n')
                time.sleep(4)
                login()
        except:
            print('\n    Cannot login! Try again...\n')
            time.sleep(4)
            login()


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
