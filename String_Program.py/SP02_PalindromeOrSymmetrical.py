#Author: Abhivaadya Sharma

# Python program to check if a string is Symmetrical and Palindrome

def check_string(s):
    n = len(s)
    mid = n // 2

    # Check Symmetry
    if n % 2 == 0:
        first_half = s[:mid]
        second_half = s[mid:]
    else:
        first_half = s[:mid]
        second_half = s[mid+1:]

    is_symmetrical = first_half == second_half

    # Check Palindrome
    is_palindrome = s == s[::-1]

    # Print results
    if is_symmetrical and is_palindrome:
        print(f"'{s}' is both Symmetrical and Palindrome")
    elif is_symmetrical:
        print(f"'{s}' is Symmetrical but not Palindrome")
    elif is_palindrome:
        print(f"'{s}' is Palindrome but not Symmetrical")
    else:
        print(f"'{s}' is neither Symmetrical nor Palindrome")


# Example usage
string = input("Enter a string: ")
check_string(string)
