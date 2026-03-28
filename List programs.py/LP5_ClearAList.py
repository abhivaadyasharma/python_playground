#Author: Abhivaadya Sharma

user_input = input("Enter elements separated by spaces: ")
user_list = user_input.split()  # Converts input to a list of strings

print("Original list:", user_list)

# To clear the list:
user_list.clear()

print("List after clearing:", user_list)