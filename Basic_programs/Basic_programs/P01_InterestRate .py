# Author: Abhivaadya Sharma

# Function to calculate Simple Interest
def simple_interest(principal, rate, time):
    interest = (principal * rate * time) / 100
    total_amount = principal + interest
    return interest, total_amount

# Function to calculate Compound Interest
def compound_interest(principal, rate, time, compounding_frequency=1):
    amount = principal * (1 + rate / (100 * compounding_frequency)) ** (compounding_frequency * time)
    interest = amount - principal
    return interest, amount

# Function to calculate Amortized Loan Payments (Monthly Payments)
def amortized_loan(principal, rate, time):
    # Monthly interest rate (annual rate divided by 12)
    monthly_rate = rate / 100 / 12
    # Number of monthly payments
    months = time * 12
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    total_payment = monthly_payment * months
    total_interest = total_payment - principal
    return monthly_payment, total_interest, total_payment

# Function to format currency values
def format_currency(amount):
    return f"₹{amount:,.2f}"

# Main function to get input and display the results
def loan_calculator():
    while True:  # Loop to keep asking for input
        print("\nLoan Calculator")
        print("1. Simple Interest")
        print("2. Compound Interest")
        print("3. Amortized Loan Payment (Monthly)")
        print("4. Exit")

        try:
            choice = int(input("Enter the number corresponding to the loan type (or 4 to exit): "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 4:
            print("Exiting the program. Goodbye!")
            break

        try:
            principal = float(input("Enter the principal amount: ₹"))
            if principal <= 0:
                print("Principal amount must be greater than zero.")
                continue
            rate = float(input("Enter the annual interest rate (in %): "))
            if rate < 0:
                print("Interest rate cannot be negative.")
                continue
            time = int(input("Enter the time period in years: "))  # Ensure the time is an integer
            if time <= 0:
                print("Time period must be greater than zero.")
                continue
        except ValueError:
            print("Please enter valid numerical values!")
            continue

        if choice == 1:
            interest, total_amount = simple_interest(principal, rate, time)
            print(f"Simple Interest: {format_currency(interest)}")
            print(f"Total Amount to be paid: {format_currency(total_amount)}")

        elif choice == 2:
            print("\nChoose compounding frequency:")
            print("1. Annually")
            print("2. Semi-Annually")
            print("3. Quarterly")
            print("4. Monthly")
            try:
                compounding_choice = int(input("Enter your choice for compounding frequency: "))
                if compounding_choice == 1:
                    compounding_frequency = 1
                elif compounding_choice == 2:
                    compounding_frequency = 2
                elif compounding_choice == 3:
                    compounding_frequency = 4
                elif compounding_choice == 4:
                    compounding_frequency = 12
                else:
                    print("Invalid choice! Defaulting to annual compounding.")
                    compounding_frequency = 1
            except ValueError:
                print("Invalid choice! Defaulting to annual compounding.")
                compounding_frequency = 1

            interest, total_amount = compound_interest(principal, rate, time, compounding_frequency)
            print(f"Compound Interest: {format_currency(interest)}")
            print(f"Total Amount to be paid: {format_currency(total_amount)}")

        elif choice == 3:
            monthly_payment, total_interest, total_payment = amortized_loan(principal, rate, time)
            print(f"Monthly Payment: {format_currency(monthly_payment)}")
            print(f"Total Interest Paid: {format_currency(total_interest)}")
            print(f"Total Payment: {format_currency(total_payment)}")

        else:
            print("Invalid choice! Please select a valid loan type.")
        
        # Ask the user if they want to continue or exit after each calculation
        continue_choice = input("\nDo you want to perform another calculation? Type 'exit' to quit or press any key to continue: ").lower()
        if continue_choice == 'exit':
            print("Exiting the program. Goodbye!")
            break

loan_calculator()
