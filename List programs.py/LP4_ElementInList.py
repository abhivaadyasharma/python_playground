#Author: Abhivaadya Sharma

# Get input from the user and convert it to a list
user_input = input("Enter elements of the list separated by spaces: ")
user_list = user_input.split()  # Creates a list of strings

element = input("Enter the element you want to check: ")

if element in user_list:
    print(f"{element} exists in the list.")
else:
    print(f"{element} does not exist in the list.")