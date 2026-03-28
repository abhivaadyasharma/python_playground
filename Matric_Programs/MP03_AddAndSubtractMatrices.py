#Autor:Abhivaadya Sharma

 
# Program to Add or Subtract two matrices (user choice)

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

# Show menu
print("\nChoose Operation:")
print("1. Add Matrices (A + B)")
print("2. Subtract Matrices (A - B)")

choice = int(input("Enter your choice (1/2): "))

# Initialize result matrix
result = [[0 for _ in range(cols)] for _ in range(rows)]

# Perform operation
if choice == 1:
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] + B[i][j]
    print_matrix(result, "Result (A + B)")

elif choice == 2:
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] - B[i][j]
    print_matrix(result, "Result (A - B)")

else:
    print("❌ Invalid choice! Please enter 1 or 2.")

