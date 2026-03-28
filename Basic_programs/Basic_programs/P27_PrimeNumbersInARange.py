# Author: Abhivaadya Sharma
# Program: Print all Prime numbers in an Interval

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def print_primes_in_interval(start, end):
    """Print all prime numbers between start and end (inclusive)."""
    if start > end:
        start, end = end, start  # swap to maintain ascending order
    print(f"Prime numbers between {start} and {end}:")
    found = False
    for num in range(start, end + 1):
        if is_prime(num):
            print(num, end=' ')
            found = True
    if not found:
        print("No prime numbers found in this interval.")
    print()

# Example usage
if __name__ == "__main__":
    try:
        start = int(input("Enter the starting number: "))
        end = int(input("Enter the ending number: "))
        print_primes_in_interval(start, end)
    except ValueError:
        print("Invalid input! Please enter valid integers.")
