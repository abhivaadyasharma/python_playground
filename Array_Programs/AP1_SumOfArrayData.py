#Author: Abhivaadya Sharma 

def sum_of_array(arr):
    """
    Returns the sum of all elements in the array.
    """
    return sum(arr)

# Input from user
n = int(input("Enter number of elements in the array: "))
arr = []

for i in range(n):
    element = int(input(f"Enter element {i+1}: "))
    arr.append(element)

# Output
print("Sum of array elements is:", sum_of_array(arr))
