# Author: Abhivaadya Sharma

def find_remainder(arr, n):
    result = 1
    for num in arr:
        result = (result * num) % n
    return result

if __name__ == "__main__":
    # Take input from user
    arr_input = input("Enter array elements separated by space: ")
    
    if not arr_input.strip():
        print("Array input cannot be empty.")
    else:
        arr = list(map(int, arr_input.strip().split()))
        try:
            n = int(input("Enter the value of n: "))
            if n == 0:
                print("n cannot be zero (division by zero error).")
            else:
                remainder = find_remainder(arr, n)
                print(f"Remainder of array multiplication divided by {n} is: {remainder}")
        except ValueError:
            print("Invalid input for n. Please enter an integer.")
