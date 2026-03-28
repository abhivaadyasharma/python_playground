# Author: Abhivaadya Sharma
# This program takes two numbers as input from the user and prints the maximum, or a message if both numbers are equal.

def maximum_of_two(a, b):
    if a == b:
        return None  # Indicating both are equal
    return a if a > b else b

# Taking input from the user
num1 = float(input("Enter first number: "))  # Input first number (Converted to float)
num2 = float(input("Enter second number: "))  # Input second number (Converted to float)

# Calling the function to find the maximum number
max_num = maximum_of_two(num1, num2)

# Displaying the result
if max_num is None:
    print("Both numbers are equal.")
else:
    print("The maximum number is:", max_num)
