#Author: Abhivaadya Sharma

def find_n_largest_elements(lst, n):
    """Return the N largest elements from the list."""
    if n <= 0:
            return []
    if n > len(lst):
            return sorted(lst, reverse=True)
    return sorted(lst, reverse=True)[:n]
    
if __name__ == "__main__":
        try:
            user_input = input("Enter numbers separated by spaces: ")
            lst = list(map(int, user_input.strip().split()))
            n = int(input("Enter N (number of largest elements to find): "))
            result = find_n_largest_elements(lst, n)
            print(f"The {n} largest elements are: {result}")
        except ValueError:
            print("Invalid input. Please enter only integers.")