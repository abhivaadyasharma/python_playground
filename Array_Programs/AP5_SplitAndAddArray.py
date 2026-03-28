# Author: Abhivaadya Sharma 

def split_and_add(arr, k):
    n = len(arr)
    if n == 0:
        return arr
    k %= n  # Handle cases where k > n
    return arr[k:] + arr[:k]

# User Input
try:
    input_str = input("Enter array elements separated by space: ")
    array = list(map(int, input_str.strip().split()))

    k = int(input("Enter the position at which to split the array: "))

    if not array:
        print("Array is empty.")
    else:
        result = split_and_add(array, k)
        print("Resulting array after split and move:", result)

except ValueError:
    print("Please enter valid integers only.")
