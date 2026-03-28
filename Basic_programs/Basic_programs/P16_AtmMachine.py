#Author:Abhivaadya Sharma

import getpass  # Used to securely take password input

class BankAccount:
    def __init__(self, name, phone, parents_name, email, address, parents_phone, password, balance=0):
        self.name = name
        self.phone = phone
        self.parents_name = parents_name
        self.email = email
        self.address = address
        self.parents_phone = parents_phone
        self.password = password
        self.balance = balance
        self.fixed_deposits = []  # List to store all fixed deposits
    
    def check_password(self):
        entered_password = getpass.getpass("Enter your password: ")
        return entered_password == self.password
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: ₹{amount}")
        else:
            print("Invalid deposit amount.")
    
    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Withdrew: ₹{amount}")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid withdrawal amount.")
    
    def check_balance(self):
        print(f"Current balance: ₹{self.balance}")
    
    def display_account_info(self):
        print("\nAccount Information:")
        print(f"Name: {self.name}")
        print(f"Phone: {self.phone}")
        print(f"Parents' Name: {self.parents_name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Parents' Phone: {self.parents_phone}")
        print(f"Current Balance: ₹{self.balance}")
    
    def create_fixed_deposit(self):
        amount = float(input("Enter the amount for Fixed Deposit: ₹"))
        duration = int(input("Enter the duration (in months): "))
        interest_rate = float(input("Enter the interest rate (in %): "))
        
        if amount <= 0 or duration <= 0 or interest_rate <= 0:
            print("Invalid input. FD creation failed.")
        else:
            # Calculate interest
            interest = (amount * interest_rate * duration) / 100
            total_amount = amount + interest
            
            # Create FixedDeposit object and store it
            fd = FixedDeposit(amount, duration, interest_rate, interest, total_amount)
            self.fixed_deposits.append(fd)
            print(f"Fixed Deposit created successfully! Total amount after {duration} months: ₹{total_amount}")
    
    def display_fixed_deposits(self):
        if self.fixed_deposits:
            print("\nFixed Deposits:")
            for fd in self.fixed_deposits:
                fd.display_fd_info()
        else:
            print("No fixed deposits found.")
    
    def edit_account_info(self):
        print("\nEdit Account Information:")
        print("1. Name")
        print("2. Phone")
        print("3. Parents' Name")
        print("4. Email")
        print("5. Address")
        print("6. Parents' Phone")
        print("7. Exit")
        
        option = input("Select the information you want to edit (1/2/3/4/5/6/7): ")
        
        if option == '1':
            self.name = input("Enter new name: ")
        elif option == '2':
            self.phone = input("Enter new phone number: ")
        elif option == '3':
            self.parents_name = input("Enter new parents' name: ")
        elif option == '4':
            self.email = input("Enter new email ID: ")
        elif option == '5':
            self.address = input("Enter new address: ")
        elif option == '6':
            self.parents_phone = input("Enter new parents' phone number: ")
        elif option == '7':
            print("Exiting edit menu.")
        else:
            print("Invalid option. Please try again.")

class FixedDeposit:
    def __init__(self, amount, duration, interest_rate, interest, total_amount):
        self.amount = amount
        self.duration = duration
        self.interest_rate = interest_rate
        self.interest = interest
        self.total_amount = total_amount

    def display_fd_info(self):
        print(f"Amount: ₹{self.amount}")
        print(f"Duration: {self.duration} months")
        print(f"Interest Rate: {self.interest_rate}%")
        print(f"Interest: ₹{self.interest}")
        print(f"Total Amount after {self.duration} months: ₹{self.total_amount}")

def atm_menu():
    print("\nATM Menu:")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Account Information")
    print("6. Create Fixed Deposit")
    print("7. View Fixed Deposits")
    print("8. Edit Account Information")
    print("9. Exit")

def create_account():
    print("\nCreate a New Bank Account:")
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    parents_name = input("Enter your parents' name: ")
    email = input("Enter your email ID: ")
    address = input("Enter your address: ")
    parents_phone = input("Enter your parents' phone number: ")
    
    password = getpass.getpass("Set a password for your account: ")
    
    # Creating the bank account object
    account = BankAccount(name, phone, parents_name, email, address, parents_phone, password, balance=0)
    print("\nAccount created successfully!")
    return account

def main():
    account = None  # Initially no account is created

    while True:
        atm_menu()
        choice = input("Select an option (1/2/3/4/5/6/7/8/9): ")
        
        if choice == '1':  # Create an account
            if account is None:
                account = create_account()
            else:
                print("Account already created! Please log in to continue.")
        elif choice == '2':  # Deposit money
            if account and account.check_password():
                amount = float(input("Enter deposit amount: ₹"))
                account.deposit(amount)
            else:
                print("Password incorrect or no account found.")
        elif choice == '3':  # Withdraw money
            if account and account.check_password():
                amount = float(input("Enter withdrawal amount: ₹"))
                account.withdraw(amount)
            else:
                print("Password incorrect or no account found.")
        elif choice == '4':  # Check balance
            if account and account.check_password():
                account.check_balance()
            else:
                print("Password incorrect or no account found.")
        elif choice == '5':  # Account Information
            if account and account.check_password():
                account.display_account_info()
            else:
                print("Password incorrect or no account found.")
        elif choice == '6':  # Create Fixed Deposit
            if account and account.check_password():
                account.create_fixed_deposit()
            else:
                print("Password incorrect or no account found.")
        elif choice == '7':  # View Fixed Deposits
            if account and account.check_password():
                account.display_fixed_deposits()
            else:
                print("Password incorrect or no account found.")
        elif choice == '8':  # Edit Account Information
            if account and account.check_password():
                account.edit_account_info()
            else:
                print("Password incorrect or no account found.")
        elif choice == '9':  # Exit the program
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            

if __name__ == "__main__":
    main()