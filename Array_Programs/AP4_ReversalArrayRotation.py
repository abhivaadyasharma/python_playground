# Author: Abhivaadya Sharma 

def reverse(arr, start, end):
    """Helper function to reverse elements in the array from index start to end."""
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

def left_rotate(arr, d):
    """Reverses the array to rotate it left by d elements."""
    n = len(arr)
    if n == 0 or d % n == 0:
        return arr  # No rotation needed

    d %= n  # In case d > n

    # Step 1: Reverse first d elements
    reverse(arr, 0, d - 1)
    # Step 2: Reverse the rest
    reverse(arr, d, n - 1)
    # Step 3: Reverse entire array
    reverse(arr, 0, n - 1)
    return arr

# User Input
try:
    input_str = input("Enter array elements separated by space: ")
    array = list(map(int, input_str.strip().split()))

    d = int(input("Enter number of positions to rotate (left rotation): "))

    if not array:
        print("Array is empty.")
    else:
        left_rotate(array, d)
        print("Rotated array:", array)

except ValueError:
    print("Please enter valid integers only.")
