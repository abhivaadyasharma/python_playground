#Author: Abhivaadya Sharma

def check_divisibility(number, divisors):
    """Check divisibility by given divisors and print the appropriate message."""
    results = []
    for divisor in divisors:
        if number % divisor == 0:
            results.append(f"divisible by {divisor}")
        else:
            results.append(f"not divisible by {divisor}")
    
    result_message = ", ".join(results)
    print(f"\n{number} is {result_message}.")

while True:
    # Ask the user for a number or exit
    user_input = input("\nEnter a number to check divisibility (or type 'exit' or 'quit' to quit): ").lower()

    # Exit if the user types 'exit' or 'quit'
    if user_input in ['exit', 'quit']:
        print("\nGoodbye! Thanks for using the program.")
        break

    try:
        # Try converting the input to an integer (only integers are valid for divisibility check)
        number = int(user_input)

        # Call the function to check divisibility (checking for divisibility by 2 and 5)
        check_divisibility(number, [2, 5])

    except ValueError:
        print("\nInvalid input! Please enter a valid number or 'exit'/'quit' to quit.")

    # Ask if the user wants to check another number
    continue_choice = input("\nDo you want to check another number? (yes/no): ").lower()
    if continue_choice != 'yes':
        print("\nGoodbye! Thanks for using the program.")
        break
