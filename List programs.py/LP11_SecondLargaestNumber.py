#Author: Abhivaaadya Sharma

def get_user_list():
    raw = input("Enter numbers separated by spaces: ")
    return [int(num) for num in raw.strip().split()]

def find_second_largest(numbers):
    if len(numbers) < 2:
        return None  # Not enough elements
    unique_numbers = list(set(numbers))  # Remove duplicates
    if len(unique_numbers) < 2:
        return None  # Not enough unique elements
    unique_numbers.sort(reverse=True)
    return unique_numbers[1]

# Main program
user_list = get_user_list()
second_largest = find_second_largest(user_list)

if second_largest is not None:
    print("Second largest number is:", second_largest)
else:
    print("Not enough unique numbers to find the second largest.")
