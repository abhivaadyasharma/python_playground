#Author: Abhivaadya Sharma

# Python program to swap two elements in a list entered by the user

# Get list input from the user (comma separated values)
user_input = input("Enter list elements separated by commas: ")
user_list = [item.strip() for item in user_input.split(",")]

# Display the original list
print("Original list:", user_list)

# Get indices to swap from the user
try:
    idx1 = int(input(f"Enter the index of the first element to swap (0 to {len(user_list)-1}): "))
    idx2 = int(input(f"Enter the index of the second element to swap (0 to {len(user_list)-1}): "))
    if 0 <= idx1 < len(user_list) and 0 <= idx2 < len(user_list):
        # Swap elements
        user_list[idx1], user_list[idx2] = user_list[idx2], user_list[idx1]
        print("List after swapping:", user_list)
    else:
        print("Error: Indices are out of range.")
except ValueError:
    print("Error: Please enter valid integer indices.")