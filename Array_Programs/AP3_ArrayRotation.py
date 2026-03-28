#Author: Abhivaadya Sharma 

# Python Program: Rotate an Array by User-Defined Positions

def rotate_array(arr, d):
    n = len(arr)
    if n == 0:
        return []
    d = d % n  # Handle cases where d > n
    return arr[d:] + arr[:d]

# Take input from the user
try:
    input_str = input("Enter array elements separated by space: ")
    array = list(map(int, input_str.strip().split()))

    d = int(input("Enter number of positions to rotate (left rotation): "))

    if not array:
        print("Array is empty.")
    else:
        rotated = rotate_array(array, d)
        print("Rotated array:", rotated)

except ValueError:
    print("Please enter valid integers only.")
