# Author: Abhivaadya Sharma

# Function to check if a number is an Armstrong number
def is_armstrong(num):
    num_str = str(num)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
    return sum_of_powers == num

# Function to get user input and validate it
def get_user_input():
    while True:
        try:
            number = int(input("Enter a number: "))
            return number
        except ValueError:
            print("Invalid input! Please enter an integer.")

# Function to display the result
def display_result(number):
    if is_armstrong(number):
        print(f"{number} is an Armstrong number.")
    else:
        print(f"{number} is not an Armstrong number.")

# Main function to run the program
def main():
    number = get_user_input()  # Get user input
    display_result(number)     # Display result

# Run the program
if __name__ == "__main__":
    main()
