#Author: Abhivaadya Sharma

def find_largest_number():
    # Get input from the user
    raw_input = input("Enter numbers separated by spaces: ")
    
    # Convert the input string into a list of numbers
    try:
        number_list = [float(num) for num in raw_input.split()]
    except ValueError:
        print("Please enter valid numbers only.")
        return

    if not number_list:
        print("The list is empty.")
        return

    # Find the largest number
    largest = max(number_list)

    # Display the result
    print("The largest number is:", largest)

# Run the function
find_largest_number()
