#Author: Abhivaadya Sharma

# Ask the user to enter list elements separated by space
input_str = input("Enter the elements of the list separated by spaces: ")

# Split the string into a list of strings, then convert each to an integer
user_list = list(map(int, input_str.split()))

# Find the sum of the elements
total_sum = sum(user_list)

# Display the result
print("Sum of elements in the list:", total_sum)