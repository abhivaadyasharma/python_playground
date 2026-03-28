#Author: Abhivaadya Sharma

# Get input from the user and convert it to a list
user_input = input("Enter elements of the list separated by spaces: ")
user_list = user_input.split()  # This creates a list of strings

# Find the length of the list
length = len(user_list)

print("The length of your list is:", length)