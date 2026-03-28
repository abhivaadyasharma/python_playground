#Autor :Abhivaadya Sharma 

# Get input from the user (comma-separated numbers)
user_input = input("Enter numbers separated by spaces: ")

# Convert the input string to a list of integers
numbers = list(map(int, user_input.split()))

# Print only the odd numbers
print("Odd numbers in the list are:")
for num in numbers:
    if num % 2 != 0:
        print(num)