#Author: Abhivaadya Sharma

# Program to find the root of any number

# Taking input from user
number = float(input("Enter the number: "))
n = float(input("Enter the root you want to find (e.g., 2 for square root, 3 for cube root): "))

# Calculating the root
root_value = number ** (1/n)

# Displaying the result
print(f"The {n} root of {number} is: {root_value}")
