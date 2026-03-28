#Author: Abhivaadya Sharma

# Get input from the user and split it into a list of integers
user_input = input("Enter numbers separated by space: ")
numbers = list(map(int, user_input.split()))

# Filter and print even numbers
print("Even numbers in the list are:")
for num in numbers:
    if num % 2 == 0:
        print(num)