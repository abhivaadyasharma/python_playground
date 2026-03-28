def fibonacci(n):
    a, b = 0, 1
    count = 0
    while True:
        print(a, end=' ')
        a, b = b, a + b
        count += 1
        if count >= n:
            break

while True:
    # Input: number of terms in the Fibonacci series
    num = int(input("Enter the number of terms: "))
    fibonacci(num)
    
    # Ask user if they want to perform again
    repeat = input("Do you want to perform again? (yes/no): ").lower()
    if repeat != 'yes':
        print("Goodbye!")
        break
