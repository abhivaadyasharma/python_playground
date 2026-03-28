# Author: Abhivaadya Sharma

while True:  # Infinite loop to allow multiple calculations
    # Step 1: Ask the user how many numbers they want to add
    try:
        num_count = int(input("How many numbers would you like to add? "))
        if num_count <= 0:
            print("Please enter a positive number.")
            continue
    except ValueError:
        print("Invalid input! Please enter an integer.")
        continue

    # Initialize a variable to store the sum
    total_sum = 0

    # Step 2: Ask the user for the numbers one by one
    for i in range(1, num_count + 1):
        try:
            number = float(input(f"Enter number {i}: "))
            total_sum += number
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            continue

    # Step 3: Print the sum
    print(f"The sum of the numbers is: {total_sum}")

    # Ask if the user wants to make another calculation
    repeat = input("\nDo you want to calculate another sum? (yes/no): ").lower()
    if repeat != "yes":
        print("Thank you for using the calculator! Goodbye.")
        break  # Exits the while loop
