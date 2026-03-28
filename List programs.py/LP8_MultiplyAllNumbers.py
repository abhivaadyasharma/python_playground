#Author: Abhivaadya Sharma

def multiply_list(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

user_input = input("Enter numbers separated by commas: ")
numbers = []

for item in user_input.split(','):
    item = item.strip()
    if item:
        try:
            numbers.append(float(item))
        except ValueError:
            print(f"Warning: '{item}' is not a valid number and will be skipped.")

if numbers:
    product = multiply_list(numbers)
    print(f"The product of the numbers is: {product}")
else:
    print("No valid numbers entered.")
