# Author: Abhivaadya Sharma
# Program to convert decimal to binary using a loop with improvements

def decimalToBinary(n, bits=None):
    '''
    Converts a non-negative integer to its binary representation as a string.
    
    Parameters:
        n (int): Non-negative decimal number.
        bits (int, optional): Minimum number of bits (pads with leading zeros if needed).
    
    Returns:
        str: Binary representation of the number.
    
    Examples:
        >>> decimalToBinary(5)
        '101'
        >>> decimalToBinary(5, 8)
        '00000101'
    '''
    if n == 0:
        binary = '0'
    else:
        binary = ''
        while n > 0:
            binary = str(n % 2) + binary
            n //= 2

    if bits:
        return binary.zfill(bits)
    return binary


def main():
    while True:
        try:
            userInput = int(input('Enter a non-negative decimal number: '))
            if userInput < 0:
                print("Please enter a non-negative number.")
            else:
                result = decimalToBinary(userInput, bits=8)
                print("Binary (8-bit padded):", result)
                
                # Ask user if they want to convert another number
                choice = input("Do you want to convert another number? (yes/no): ").strip().lower()
                if choice not in ['yes', 'y']:
                    print("Thanks for using the converter!")
                    break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


if __name__ == '__main__':
    main()