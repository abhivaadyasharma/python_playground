#Author: Abhivaadya Sharma 

# Python Program: Find the Largest Element in an Array (User Input)

def find_largest_element(arr):
    if not arr:
        return None

    max_element = arr[0]
    for num in arr[1:]:
        if num > max_element:
            max_element = num
    return max_element

# Take input from user
try:
    input_str = input("Enter numbers separated by space: ")
    array = list(map(int, input_str.strip().split()))

    if not array:
        print("Array is empty.")
    else:
        largest = find_largest_element(array)
        print("The largest element is:", largest)

except ValueError:
    print("Please enter valid integers only.")
