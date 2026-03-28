#Author:Abhivaadya Sharma

# Program to add two matrices entered by user

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

# Take input for matrix size
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

# Input matrices
A = input_matrix(rows, cols, "A")
B = input_matrix(rows, cols, "B")

# Initialize result matrix
result = [[0 for _ in range(cols)] for _ in range(rows)]

# Add matrices
for i in range(rows):
    for j in range(cols):
        result[i][j] = A[i][j] + B[i][j]

# Print all matrices
print_matrix(A, "Matrix A")
print_matrix(B, "Matrix B")
print_matrix(result, "Resultant Matrix (A + B)")
set