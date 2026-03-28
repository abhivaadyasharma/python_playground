import hashlib
import random
import time
import base64
import re
from datetime import datetime

# Bank Information
BANK_NAME = "AVS Bank Limited"
BANK_TAGLINE = "We manage your finance"

# Function for encryption and decryption (simple encryption)
def encrypt_data(data, key):
    hash_object = hashlib.sha256((key + data).encode())
    encrypted_data = base64.urlsafe_b64encode(hash_object.digest())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    return "Decryption not supported with this method."

# Class for managing user accounts
class BankAccount:
    def __init__(self, account_number, account_type, balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.transactions = []
        self.loan_balance = 0
        self.interest_rate = 0
        self.interest_calculation_type = "simple"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount} at {datetime.now()}")
            print(f"Deposit successful: ${amount}")
            return True
        print("Deposit amount must be greater than zero.")
        return False

    def withdraw(self, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount} at {datetime.now()}")
            print(f"Withdrawal successful: ${amount}")
            return True
        print("Insufficient funds or invalid amount.")
        return False

    def transfer(self, to_account, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            to_account.deposit(amount)
            self.transactions.append(f"Transferred ${amount} to Account {to_account.account_number} at {datetime.now()}")
            print(f"Transfer successful: ${amount}")
            return True
        print("Insufficient funds or invalid transfer amount.")
        return False

    def apply_interest(self):
        if self.account_type == "savings" and self.balance > 0:
            if self.interest_calculation_type == "simple":
                interest = self.balance * self.interest_rate
            else:  # compound interest
                interest = self.balance * (1 + self.interest_rate) ** 1 - self.balance
            self.balance += interest
            self.transactions.append(f"Applied interest at {datetime.now()}: ${interest}")
            return True
        print("Interest can only be applied to savings accounts with a positive balance.")
        return False

    def get_transaction_history(self):
        return self.transactions

    def create_fixed_deposit(self, amount, interest_rate, months):
        if amount > 0:
            fd_balance = amount * (1 + interest_rate / 100) ** months
            self.balance -= amount
            self.transactions.append(f"Created Fixed Deposit of ${amount} for {months} months at {interest_rate}% interest.")
            return fd_balance
        print("Amount must be greater than zero.")
        return 0

    def create_recurring_deposit(self, monthly_amount, interest_rate, months):
        if monthly_amount > 0:
            rd_balance = monthly_amount * months * (1 + interest_rate / 100)
            self.transactions.append(f"Created Recurring Deposit of ${monthly_amount} for {months} months at {interest_rate}% interest.")
            return rd_balance
        print("Monthly deposit must be greater than zero.")
        return 0

    def apply_for_loan(self, amount, interest_rate, term):
        if amount > 0:
            self.loan_balance = amount * (1 + interest_rate * term)
            self.transactions.append(f"Loan of ${amount} applied with {interest_rate}% interest rate for {term} years.")
            print(f"Loan application successful: ${amount} at {interest_rate}% for {term} years.")
            return True
        print("Loan amount must be greater than zero.")
        return False

    def repay_loan(self, amount):
        if amount > 0 and amount <= self.loan_balance:
            self.loan_balance -= amount
            self.transactions.append(f"Loan repayment of ${amount} made.")
            print(f"Loan repayment successful: ${amount}")
            return True
        print("Invalid loan repayment amount.")
        return False

# Class for managing users (Registration, Login)
class BankUser:
    def __init__(self, full_name, address, dob, phone, email, ssn, password):
        self.full_name = full_name
        self.address = address
        self.dob = dob
        self.phone = phone
        self.email = email
        self.ssn = ssn
        self.password_hash = self.hash_password(password)
        self.account_number = self.generate_account_number()
        self.accounts = []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def generate_account_number(self):
        return random.randint(1000000000, 9999999999)

    def create_account(self, account_type):
        new_account = BankAccount(self.account_number, account_type)
        self.accounts.append(new_account)
        return new_account

# Class for managing admins (Admin login, account creation, deletion)
class BankAdmin:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def delete_user_account(self, user_db, account_number):
        user = user_db.get(account_number)
        if user:
            del user_db[account_number]
            print(f"Account {account_number} deleted successfully.")
            return True
        print("Account not found.")
        return False

    def view_account_summary(self, user_db):
        print("\n=== Account Summary ===")
        for account_number, user in user_db.items():
            print(f"Account Number: {user.account_number}")
            print(f"Name: {user.full_name}")
            print(f"Email: {user.email}")
            print(f"Transactions: {user.get_transaction_history()}")
            print("-" * 30)

# Class for managing employees (Employee login and limited functionality)
class BankEmployee:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def view_account_info(self, user):
        for account in user.accounts:
            print(f"Account Number: {account.account_number}")
            print(f"Account Type: {account.account_type}")
            print(f"Balance: ${account.balance}")
            print(f"Transactions: {account.get_transaction_history()}")
            print("-" * 30)

    def assist_with_loan(self, user):
        print("\n--- Loan Assistance ---")
        print(f"Loan Balance: ${user.loan_balance}")
        print(f"Loan Transactions: {user.get_transaction_history()}")

# Dummy data (would typically be retrieved from a database)
user_db = {}
admin_db = {"admin": BankAdmin("admin", "admin123")}
employee_db = {
    "employee1": BankEmployee("employee1", "password1"),
    "employee2": BankEmployee("employee2", "password2"),
}
encryption_key = "secretkey"  # You should securely store this key

# Validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Validate phone number format (basic)
def is_valid_phone(phone):
    return re.match(r"\+?[0-9]{10,15}", phone)

# Functions for User Registration & Authentication with password confirmation
def user_registration():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    full_name = input("Enter Full Name: ")
    address = input("Enter Address: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    phone = input("Enter Phone Number: ")
    while not is_valid_phone(phone):
        print("Invalid phone number format. Try again.")
        phone = input("Enter Phone Number: ")
    
    email = input("Enter Email: ")
    while not is_valid_email(email):
        print("Invalid email format. Try again.")
        email = input("Enter Email: ")

    ssn = input("Enter Social Security Number (or equivalent): ")

    while True:
        password = input("Enter Password: ")
        confirm_password = input("Confirm Password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")
    
    user = BankUser(full_name, address, dob, phone, email, ssn, password)
    user_db[user.account_number] = user
    print("User registered successfully!")
    return user

def admin_registration():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    admin_username = input("Enter Admin Username: ")
    while True:
        admin_password = input("Enter Admin Password: ")
        confirm_admin_password = input("Confirm Admin Password: ")
        if admin_password == confirm_admin_password:
            break
        else:
            print("Passwords do not match. Please try again.")
    
    admin_db[admin_username] = BankAdmin(admin_username, admin_password)
    print("Admin registered successfully!")

def employee_registration():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    employee_username = input("Enter Employee Username: ")
    while True:
        employee_password = input("Enter Employee Password: ")
        confirm_employee_password = input("Confirm Employee Password: ")
        if employee_password == confirm_employee_password:
            break
        else:
            print("Passwords do not match. Please try again.")
    
    employee_db[employee_username] = BankEmployee(employee_username, employee_password)
    print("Employee registered successfully!")

# Functions for Admin login
def admin_login():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    admin = admin_db.get(username)
    if admin and admin.verify_password(password):
        print("Admin login successful!")
        return admin
    else:
        print("Invalid credentials.")
        return None

# Functions for Employee login
def employee_login():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    username = input("Enter Employee Username: ")
    password = input("Enter Employee Password: ")
    employee = employee_db.get(username)
    if employee and employee.verify_password(password):
        print("Employee login successful!")
        return employee
    else:
        print("Invalid credentials.")
        return None

# Functions for Transaction Management
def deposit_account(user):
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    account_number = int(input("Enter Account Number to Deposit into: "))
    amount = float(input("Enter Deposit Amount: "))
    for account in user.accounts:
        if account.account_number == account_number:
            if account.deposit(amount):
                print(f"Deposited ${amount} into account {account_number}.")
            else:
                print("Invalid deposit amount.")
            return
    print("Account not found.")

def withdraw_account(user):
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    account_number = int(input("Enter Account Number to Withdraw from: "))
    amount = float(input("Enter Withdrawal Amount: "))
    for account in user.accounts:
        if account.account_number == account_number:
            if account.withdraw(amount):
                print(f"Withdrew ${amount} from account {account_number}.")
            else:
                print("Insufficient funds.")
            return
    print("Account not found.")

def transfer_account(user):
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    from_account_number = int(input("Enter Account Number to Transfer from: "))
    to_account_number = int(input("Enter Account Number to Transfer to: "))
    amount = float(input("Enter Transfer Amount: "))
    from_account = None
    to_account = None
    for account in user.accounts:
        if account.account_number == from_account_number:
            from_account = account
        if account.account_number == to_account_number:
            to_account = account
    if from_account and to_account:
        if from_account.transfer(to_account, amount):
            print(f"Transferred ${amount} from account {from_account_number} to {to_account_number}.")
        else:
            print("Insufficient funds.")
    else:
        print("Account not found.")

# Functions for User Login
def user_login():
    print("\n=== Welcome to the AVS Bank Limited ===")
    print(BANK_TAGLINE)
    account_number = int(input("Enter Account Number: "))
    password = input("Enter Password: ")
    user = user_db.get(account_number)
    if user and user.verify_password(password):
        print("User login successful!")
        return user
    else:
        print("Invalid credentials.")
        return None

# Employee Menu
def employee_menu(employee):
    while True:
        print("\n=== Welcome to the AVS Bank Limited ===")
        print(BANK_TAGLINE)
        print("\n=== Employee Menu ===")
        print("1. View User Account Info")
        print("2. Assist with Deposit/Withdrawal")
        print("3. Issue New Account")
        print("4. Assist with Loan")
        print("5. Exit")

        employee_choice = input("Enter your choice: ")

        if employee_choice == "1":
            account_number = int(input("Enter Account Number to view: "))
            user = user_db.get(account_number)
            if user:
                employee.view_account_info(user)
            else:
                print("Account not found.")
        elif employee_choice == "2":
            user = user_login()  # Now calls the user_login function
            if user:
                print("\n1. Deposit\n2. Withdraw")
                action_choice = input("Enter choice: ")
                if action_choice == "1":
                    deposit_account(user)
                elif action_choice == "2":
                    withdraw_account(user)
        elif employee_choice == "3":
            user_registration()
        elif employee_choice == "4":
            user = user_login()  # Get user for loan assistance
            if user:
                employee.assist_with_loan(user)
        elif employee_choice == "5":
            print("Exiting employee menu...")
            break
        else:
            print("Invalid option.")

# Main Program
def main():
    while True:
        print("\n=== Welcome to the AVS Bank Limited ===")
        print(BANK_TAGLINE)
        print("1. Register as User")
        print("2. Register as Admin")
        print("3. Register as Employee")
        print("4. User Login")
        print("5. Admin Login")
        print("6. Employee Login")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_registration()
        elif choice == "2":
            admin_registration()
        elif choice == "3":
            employee_registration()
        elif choice == "4":
            user = user_login()  # Calls the user login for users
            if user:
                while True:
                    print("\n=== User Menu ===")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. View Transaction History")
                    print("5. Create Fixed Deposit")
                    print("6. Create Recurring Deposit")
                    print("7. Apply for Loan")
                    print("8. Repay Loan")
                    print("9. Exit")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        deposit_account(user)
                    elif user_choice == "2":
                        withdraw_account(user)
                    elif user_choice == "3":
                        transfer_account(user)
                    elif user_choice == "4":
                        account_number = int(input("Enter Account Number to view transaction history: "))
                        for account in user.accounts:
                            if account.account_number == account_number:
                                print(account.get_transaction_history())
                                break
                    elif user_choice == "5":
                        account_number = int(input("Enter Account Number for FD: "))
                        amount = float(input("Enter FD Amount: "))
                        interest_rate = float(input("Enter Interest Rate: "))
                        months = int(input("Enter Duration in Months: "))
                        for account in user.accounts:
                            if account.account_number == account_number:
                                fd_balance = account.create_fixed_deposit(amount, interest_rate, months)
                                print(f"Fixed Deposit created with final balance: ${fd_balance}")
                                break
                    elif user_choice == "6":
                        account_number = int(input("Enter Account Number for RD: "))
                        monthly_amount = float(input("Enter Monthly Deposit Amount: "))
                        interest_rate = float(input("Enter Interest Rate: "))
                        months = int(input("Enter Duration in Months: "))
                        for account in user.accounts:
                            if account.account_number == account_number:
                                rd_balance = account.create_recurring_deposit(monthly_amount, interest_rate, months)
                                print(f"Recurring Deposit created with final balance: ${rd_balance}")
                                break
                    elif user_choice == "7":
                        account_number = int(input("Enter Account Number for Loan: "))
                        amount = float(input("Enter Loan Amount: "))
                        interest_rate = float(input("Enter Loan Interest Rate: "))
                        term = int(input("Enter Loan Term (in years): "))
                        for account in user.accounts:
                            if account.account_number == account_number:
                                account.apply_for_loan(amount, interest_rate, term)
                                break
                    elif user_choice == "8":
                        account_number = int(input("Enter Account Number to repay loan: "))
                        amount = float(input("Enter Loan Repayment Amount: "))
                        for account in user.accounts:
                            if account.account_number == account_number:
                                account.repay_loan(amount)
                                break
                    elif user_choice == "9":
                        break
                    else:
                        print("Invalid option.")
        elif choice == "5":
            admin = admin_login()
            if admin:
                while True:
                    print("\n=== Admin Menu ===")
                    print("1. Delete User Account")
                    print("2. View Account Summary")
                    print("3. Exit")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        account_number = int(input("Enter Account Number to delete: "))
                        admin.delete_user_account(user_db, account_number)
                    elif admin_choice == "2":
                        admin.view_account_summary(user_db)
                    elif admin_choice == "3":
                        break
                    else:
                        print("Invalid option.")
        elif choice == "6":
            employee = employee_login()
            if employee:
                employee_menu(employee)       
        elif choice == "7":
            print("Exiting the bank system...")    
            break
        else:
            print("Invalid option.")

# Run the program
if __name__ == "__main__":
    main()
