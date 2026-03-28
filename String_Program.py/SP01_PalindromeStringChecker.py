#Author: Abhivaadya Sharma

# Palindrome Check Program

text = input("Enter a string: ")

# Remove spaces and make lowercase for accurate checking
cleaned = text.replace(" ", "").lower()

if cleaned == cleaned[::-1]:
    print("Yes, it's a Palindrome!")
else:
    print("No, it's not a Palindrome.")

\

