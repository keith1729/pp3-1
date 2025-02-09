# The Bank
The Bank is an online banking application developed with Python which gives the user the ability to create an account, login to their account, deposit and withdraw from their balance, and see their account details.

<div align="center">
  <img src="assets/responsive.PNG" alt="Responsive Display">
</div>

## Table of contents:

<ol>
    <li>UX</li>
    <li>Features</li>
    <li>Technologies Used</li>
    <li>Testing</li>
    <li>Deployment</li>
    <li>Credits</li>
<ol>

## 1. UX

The users for The Bank application are:
- Anyone who wishes to interact with an online banking app
- People that wish to use a banking app built with Python

<div align="center">
  <img src="assets/flow_chart.PNG" alt="Flow Chart">
</div>

## 2. Features

The welcome page displays the logo for the application and two options for the user,
the first option is to login for existing account holders and the second option is 
to create a new account for new users.
- To create a new account the user needs to enter a username and an account number
and pin will be generated
- The login option is for returning users with accounts already set up, the user is
prompted for their username and pin and these are used to validate the users login 

<div align="center">
  <img src="assets/welcome_page.PNG" alt="Welcome page">
</div>
<div align="center">
  <img src="assets/create_new_acc.PNG" alt="Create account">
</div>
<div align="center">
  <img src="assets/login.PNG" alt="Login">
</div>

- The options page gives the user a list of four options once logged in. Deposit, withdraw, show account
 details and exit.

<div align="center">
  <img src="assets/options.PNG" alt="Options page">
</div>

- The deposit feature lets the user add to their balance

<div align="center">
  <img src="assets/deposit.PNG" alt="Deposit feature">
</div>

- The withdraw feature lets the user take away from their balance

<div align="center">
  <img src="assets/withdraw.PNG" alt="Withdraw feature">
</div>

- The account details feature allows the use to see all of their account data

<div align="center">
  <img src="assets/acc_details.PNG" alt="Account details">
</div>

- The exit option allows the user to exit options and return to welcome page

<div align="center">
  <img src="assets/exit.PNG" alt="Exit">
</div>

## 3. Technologies Used

- Python is the language that was used to develope this banking application
- Google sheets is used to store the user accounts data
- Github for version control

## 4. Testing

- Validator testing
The Python code was passed through the pep8 Python Linter validator and showed some whitespace warnings.

- Bugs
Errors were not being caught and forcing the programme to crash, while loops with try and except were
used to catch any errors from users inputing unsuitable data.

- Manual testing
Whenever a new feature was developed into the app it was manually tested.

## 5. Deployment

- Heroku deployment procedure
Login to Heroku
Go to 'Create new app'
Enter a unique application name, select your region and click 'Create app'
Go to 'settings' tab
Under 'Config Vars' click 'Reveal Config Vars'
Add the JSPN CREDS file
Add PORT 8000
Add 'heroku/python' and 'heroku/node.js' to the 'Buildpacks'
Click the 'Deploy' tab.
In the 'Deployment method' section select 'GitHub'
Search for the repo name and click 'connect'
Under 'Automatic deploys' click 'Enable Automatic Deploys'

## 6. Credits

- Mentor for giving assistance with code 
- Facilitator for educational resources
- Youtube for tutorials
- ChatGPT for helping to understand pythonic code
- The Love Sandwiches walk-through project
- The Black python formatter was installed and used to format code