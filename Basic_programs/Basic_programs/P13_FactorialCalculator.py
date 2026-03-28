import sys
import math
from functools import lru_cache

# Using LRU cache to store previously computed factorials for faster results
@lru_cache(maxsize=None)  # Infinite cache size for factorial
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

# Iterative approach for factorial calculation (avoiding recursion depth issues)
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Enhanced input validation function
def get_valid_input():
    while True:
        try:
            num = int(input("Enter a non-negative integer to calculate factorial: "))
            if num < 0:
                raise ValueError("Input cannot be negative.")
            return num
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

# Main function to handle the factorial calculation
def main():
    # Infinite loop until the user chooses to quit
    while True:
        print("Welcome to the Enhanced Factorial Program!")
        
        # Get valid user input
        number = get_valid_input()
        
        # Ask user for the preferred method
        method = input("Choose the method (recursive/iterative): ").strip().lower()
        
        if method == "recursive":
            print(f"Calculating factorial using recursive method...")
            result = factorial_recursive(number)
        elif method == "iterative":
            print(f"Calculating factorial using iterative method...")
            result = factorial_iterative(number)
        else:
            print("Invalid method selected, defaulting to recursive method.")
            result = factorial_recursive(number)
        
        print(f"The factorial of {number} is {result}")
        
        # If the number is large, show that the result can be enormous
        if number > 20:  # Can be adjusted based on requirements
            print(f"Note: Factorial of {number} is a large number.")
        
        # Ask if the user wants to calculate another factorial
        continue_prompt = input("\nDo you want to calculate another factorial? (yes/no): ").strip().lower()
        
        if continue_prompt != "yes":
            print("Goodbye!")
            break  # Exit the loop and end the program

# Running the main program
if __name__ == "__main__":
    sys.setrecursionlimit(2000)  # Allow larger recursion depth for bigger factorials
    main()
