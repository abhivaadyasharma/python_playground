# Author: Abhivaadya Sharma

def check_even_odd(number):
    """Check whether the number is even or odd."""
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

def main():
    print("Welcome to the Even/Odd Checker!")
    print("You can enter any number to check if it's even or odd.")
    print("Type 'exit' at any time to quit the program.")

    while True:
        # Prompt user for input with better instructions
        user_input = input("\nPlease enter a number to check (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("\nThank you for using the Even/Odd Checker. Goodbye!")
            break
        
        # Try to convert the input into an integer, and handle invalid inputs
        try:
            num = int(user_input)
            # Check if the number is even or odd
            result = check_even_odd(num)
            print(f"\n--- Result ---\nThe number {num} is {result}.\n")
        except ValueError:
            print("\nOops! That's not a valid number. Please enter a valid integer or 'exit' to quit.")
        
        # Ask the user if they want to continue or exit with clearer instructions
        continue_choice = input("\nWould you like to check another number? (yes to continue, no to exit): ").strip().lower()
        if continue_choice != 'yes':
            print("\nThank you for using the Even/Odd Checker. Goodbye!")
            break

# Run the main function
if __name__ == "__main__":
    main()
