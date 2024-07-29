import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz
import time
import random
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

            username = input('\n>> \n')

            if username.strip():  
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
            username_entered = input('\n    Enter Username: \n')
            time.sleep(1)
            pin_entered = input('\n    Enter Pin: \n')

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
                options(user_account)
                break           
            else:
                print('\n    Cannot login! Please check your credentials and try again...\n')
                time.sleep(4)
                login()
        except ValueError:
            print('\n    Cannot login! Please check your credentials and try again...\n')
            time.sleep(4)
            login()


def options(user_account):

    while True:
        try:
            clear_screen()
            time.sleep(2)
            print(f'''{Fore.YELLOW}{logo}''')
            time.sleep(2)
            characters(f'''{Fore.WHITE}
    Welcome {user_account.username}!
                
    Please choose one of the following options:

    [1] Deposit
    [2] Withdraw
    [3] Show Account Details
    [4] Exit
            ''')

            option = int(input('\n>> \n'))

            if option == 1:
                clear_screen()
                time.sleep(2)
                print(f'''{Fore.YELLOW}{logo}''')
                time.sleep(2)
                characters(f'''{Fore.WHITE}
    To deposit into {user_account.username}'s account
                ''')
                deposit_amount = float(input('\n    Enter your deposit amount: €\n'))
                user_account.deposit(deposit_amount)
                time.sleep(3)
                characters('''
    Deposit Successful!
                ''')
                time.sleep(2)
                characters(f'''
    New Balance: €{user_account.balance}    
                ''')
                cell = accounts_worksheet.find(user_account.username)
                accounts_worksheet.update_cell(cell.row, 4, user_account.balance)
                proceed(user_account)
                break
            elif option == 2:
                clear_screen()
                time.sleep(2)
                print(f'''{Fore.YELLOW}{logo}''')
                time.sleep(2)
                characters(f'''{Fore.WHITE}
    To withdraw from {user_account.username}'s account
                ''')
                withdraw_amount = float(input('\n    Enter your withdraw amount: €\n'))
                user_account.withdraw(withdraw_amount)
                time.sleep(3)
                characters('''
    Withdrawal Successful!
                ''')
                time.sleep(2)
                characters(f'''
    New Balance: €{user_account.balance}
                ''')
                cell = accounts_worksheet.find(user_account.username)
                accounts_worksheet.update_cell(cell.row, 4, user_account.balance)
                proceed(user_account)
                break
            elif option == 3:
                clear_screen()
                time.sleep(2)
                print(f'''{Fore.YELLOW}{logo}''')
                time.sleep(2)
                characters(f'''{Fore.WHITE}
    {user_account.username} your Account Details are as follows:

    Username: {user_account.username}
    Account Number: {user_account.account_number}
    Pin: {user_account.pin}
    Current Balance: €{user_account.balance}
                ''')
                time.sleep(2)
                proceed(user_account)
                break
            elif option == 4:
                clear_screen()
                time.sleep(2)
                print(f'''{Fore.YELLOW}{logo}''')
                time.sleep(2)
                characters(f'''{Fore.WHITE}
    Thank you {user_account.username} for using The Bank!
                
                ''')
                time.sleep(6)
                welcome()
                break
            else:
                print('\nPlease enter a valid option (1-4)\n')
                time.sleep(4)
                options(user_account)
        except ValueError:
            print('\nInvalid input. Please enter a number (1-4)\n')
            time.sleep(4)
            options(user_account)


def proceed(user_account):
    while True:
        try:
            characters('''
    Would you like to continue to your options page?

    Please choose one of the following:

    [1] Options
    [2] Exit
            ''')
            
            option = int(input('\n>> \n'))

            if option == 1:
                options(user_account)
                break
            elif option ==2:
                characters(f'''
    Thank you {user_account.username} for using The Bank!
                
                ''')
                time.sleep(6)
                welcome()
                break
            else:
                print('\nPlease enter a valid option (1-2)\n')
                time.sleep(4)
                proceed(user_account)
        except ValueError:
            print('\nInvalid input. Please enter a number (1-2)\n')
            time.sleep(4)
            proceed(user_account)


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
            
            login_option = int(input('\n>> \n'))
            
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
