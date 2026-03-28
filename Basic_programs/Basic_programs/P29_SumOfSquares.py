#Author: Abhivaadya Sharma

def sum_of_squares_formula(n):
    return n * (n + 1) * (2 * n + 1) // 6

# Example usage:
n = int(input("Enter a number: "))
print(f"Sum of squares of first {n} natural numbers is {sum_of_squares_formula(n)}")
