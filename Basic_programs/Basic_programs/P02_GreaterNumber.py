#Author: Abhivaadya Sharma

# Loop to keep asking for numbers until the user decides to stop
while True:
    # Get input from the user for two numbers
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    # Compare the numbers and print the greater one
    if num1 > num2:
        print(f"The greater number is: {num1}")
    elif num2 > num1:
        print(f"The greater number is: {num2}")
    else:
        print("Both numbers are equal.")

    # Ask the user if they want to continue
    repeat = input("Do you want to compare another pair of numbers? (yes/no): ").lower()

    if repeat != 'yes':
        print("Thank you for using the program!")
        break  # Exit the loop if the user does not want to continue

