#Author: Abhivaadya Sharma 

def cube_sum(n):
    """
    Calculate the sum of cubes of first n natural numbers.
    Formula: (n(n+1)/2)^2
    """
    total = (n * (n + 1) // 2) ** 2
    return total

# Example usage:
n = int(input("Enter a number: "))
print(f"Sum of cubes of first {n} natural numbers is:", cube_sum(n))
