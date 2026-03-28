#Author: Abhivaadya Sharma

# Ask user for matrix
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

print("Enter the matrix elements row-wise:")
matrix = [[int(input(f"Element [{i+1},{j+1}]: ")) for j in range(cols)] for i in range(rows)]

# Transpose in one line
transpose = [list(row) for row in zip(*matrix)]

print("\nOriginal Matrix:")
for r in matrix:
    print(r)

print("\nTranspose Matrix:")
for r in transpose:
    print(r)
