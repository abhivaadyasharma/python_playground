#Author: Abhivaadya Sharma

def find_smallest_number():
    # Get user input as a string and split by spaces or commas
    raw_input = input("Enter numbers separated by spaces or commas: ")

    # Replace commas with spaces, split into list, and convert each item to a number
    number_list = [float(num) for num in raw_input.replace(',', ' ').split()]

    # Find the smallest number
    smallest = min(number_list)

    print("The smallest number is:", smallest)

# Run the function
find_smallest_number()
