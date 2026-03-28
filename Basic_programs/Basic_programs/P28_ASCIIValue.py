#Autor:Abhivaadya Sharma

# Program to print ASCII value of a character

def print_ascii():
    char = input("Enter a single character: ")

    # Check if input is exactly one character
    if len(char) != 1:
        print("❌ Please enter exactly ONE character.")
        return

    ascii_value = ord(char)
    print(f"✅ The ASCII value of '{char}' is: {ascii_value}")

# Run the function
print_ascii()
