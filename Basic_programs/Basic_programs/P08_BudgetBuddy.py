# Author: Abhivaadya Sharma

# Budget Management Program

class BudgetManager:
    def __init__(self):
        self.budget = {}
        self.expenses = {}

    def set_budget(self):
        print("\nSetting up your budget!")
        while True:
            try:
                num_categories = int(input("How many categories would you like to set? "))
                if num_categories <= 0:
                    print("Please enter a positive number for categories.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        for _ in range(num_categories):
            category = input("\nEnter the category name (e.g., Food, Transport): ")
            while True:
                try:
                    amount = float(input(f"Enter your budget for {category}: $"))
                    if amount < 0:
                        print("Budget cannot be negative. Please try again.")
                    else:
                        self.budget[category] = amount
                        self.expenses[category] = 0
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    def add_expense(self):
        print("\nRecording an expense!")
        for category in self.budget:
            while True:
                try:
                    expense = float(input(f"Enter amount spent on {category}: $"))
                    if expense < 0:
                        print("Expense cannot be negative. Please try again.")
                    else:
                        self.expenses[category] += expense
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    def view_report(self):
        print("\nYour Budget vs Expenses Report:")
        print(f"{'Category':<20}{'Budget($)':<15}{'Spent($)':<15}{'Remaining($)':<15}")
        print("-" * 65)

        for category in self.budget:
            remaining = self.budget[category] - self.expenses[category]
            print(f"{category:<20}{self.budget[category]:<15}{self.expenses[category]:<15}{remaining:<15}")

    def check_budget_status(self):
        print("\nChecking Budget Status:")
        for category in self.budget:
            if self.expenses[category] > self.budget[category]:
                print(f"Warning! You've exceeded the budget for {category} by ${self.expenses[category] - self.budget[category]:.2f}")
            else:
                remaining = self.budget[category] - self.expenses[category]
                print(f"You have ${remaining:.2f} remaining in the {category} budget.")

def main():
    budget_manager = BudgetManager()

    # Set up the budget
    budget_manager.set_budget()

    while True:
        print("\nChoose an option:")
        print("1. Add Expense")
        print("2. View Budget and Expenses")
        print("3. Check Budget Status")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            budget_manager.add_expense()
        elif choice == '2':
            budget_manager.view_report()
        elif choice == '3':
            budget_manager.check_budget_status()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
