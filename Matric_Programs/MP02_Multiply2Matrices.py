#Author: Abhivaadya Sharma

# Program to multiply two matrices entered by user

# Function to take matrix input
def input_matrix(rows, cols, name):
    print(f"\nEnter elements of Matrix {name}:")
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = int(input(f"Enter element {name}[{i+1}][{j+1}]: "))
            row.append(val)
        matrix.append(row)
    return matrix

# Function to print matrix neatly
def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        print("  ".join(str(x) for x in row))

# Take input for matrix sizes
r1 = int(input("Enter number of rows for Matrix A: "))
c1 = int(input("Enter number of columns for Matrix A: "))
r2 = int(input("Enter number of rows for Matrix B: "))
c2 = int(input("Enter number of columns for Matrix B: "))

# Check multiplication condition
if c1 != r2:
    print("Matrix multiplication not possible! (columns of A must equal rows of B)")
else:
    # Input matrices
    A = input_matrix(r1, c1, "A")
    B = input_matrix(r2, c2, "B")

    # Initialize result matrix
    result = [[0 for _ in range(c2)] for _ in range(r1)]

    # Multiply matrices
    for i in range(r1):
        for j in range(c2):
            for k in range(c1):  # or r2, since c1 == r2
                result[i][j] += A[i][k] * B[k][j]

    # Print matrices
    print_matrix(A, "Matrix A")
    print_matrix(B, "Matrix B")
    print_matrix(result, "Resultant Matrix (A × B)")
