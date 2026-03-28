# Author: Abhivaadya Sharma

def check_prime(number):
    """Function to check if a number is prime."""
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def main():
    print("Welcome to the Prime Number Checker!")
    print("You can check if a number is prime by entering a number.")
    print("Type 'exit' at any time to quit the program.")
    
    while True:
        # Ask user for input
        user_input = input("\nEnter a number to check if it's prime (or type 'exit' to quit): ")
        
        # Allow user to exit gracefully
        if user_input.lower() == 'exit':
            print("\nThank you for using the Prime Number Checker! Goodbye.")
            break
        
        # Check if input is a valid number
        try:
            num = int(user_input)
            
            # Check if the number is prime
            if check_prime(num):
                print(f"\nThe number {num} is prime!")
            else:
                print(f"\nThe number {num} is not prime.")
        except ValueError:
            print("\nOops! That wasn't a valid number. Please enter an integer or 'exit' to quit.")
        
        # Ask if the user wants to continue or exit
        continue_choice = input("\nDo you want to check another number? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("\nThank you for using the Prime Number Checker! Goodbye.")
            break

# Run the main function
if __name__ == "__main__":
    main()
