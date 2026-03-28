# Author: Abhivaadya Sharma
# This program converts the given binary number to its decimal equivalent

def binaryToDecimal(binary):
    '''This function calculates the decimal equivalent of a given binary number'''
    binary1 = binary
    decimal, i = 0, 0
    while binary != 0:
        dec = binary % 10
        decimal += dec * pow(2, i)
        binary //= 10
        i += 1
    print('Decimal equivalent of {} is {}'.format(binary1, decimal))

def isValidBinary(binaryStr):
    '''Check if a given string contains only 0s and 1s'''
    return all(char in '01' for char in binaryStr)

if __name__ == '__main__':
    while True:
        userInput = input('Enter the binary number to check its decimal equivalent: ').strip()
        
        if not userInput.isdigit() or not isValidBinary(userInput):
            print("Invalid input. Please enter a binary number containing only 0s and 1s.")
            continue

        binaryToDecimal(int(userInput))
        
        choice = input("Do you want to convert another binary number? (yes/no): ").strip().lower()
        if choice not in ['yes', 'y']:
            print("Thank you for using the binary to decimal converter!")
            break
