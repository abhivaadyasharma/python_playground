# Author: Abhivaadya Sharma

def square():
    side = float(input("What is the length of side? "))
    perimeter_of_square = 4 * side
    print("Perimeter of square:", perimeter_of_square)

def rectangle():
    length = float(input("What is length of rectangle? "))
    breadth = float(input("What is breadth of rectangle? "))
    perimeter_of_rectangle = 2 * (length + breadth)
    print("Perimeter of rectangle:", perimeter_of_rectangle)

def triangle():
    number_1 = float(input("What is length of First side? ")) 
    number_2 = float(input("What is length of Second side? ")) 
    number_3 = float(input("What is length of Third side? ")) 
    perimeter_of_triangle = number_1 + number_2 + number_3
    print("Perimeter of triangle:", perimeter_of_triangle)

def circle():
    radius = float(input("What is length of radius? ")) 
    perimeter_of_circle = 2 * 3.14159265359 * radius
    print("Perimeter of circle:", perimeter_of_circle)

def parallelogram():
    side_1 = float(input("What is the length of the first side? "))
    side_2 = float(input("What is the length of the second side? "))
    perimeter_of_parallelogram = 2 * (side_1 + side_2)
    print("Perimeter of parallelogram:", perimeter_of_parallelogram)

def rhombus():
    side = float(input("What is the length of a side? "))
    perimeter_of_rhombus = 4 * side
    print("Perimeter of rhombus:", perimeter_of_rhombus)

def trapezoid():
    side_1 = float(input("What is the length of the first side? "))
    side_2 = float(input("What is the length of the second side? "))
    side_3 = float(input("What is the length of the third side? "))
    side_4 = float(input("What is the length of the fourth side? "))
    perimeter_of_trapezoid = side_1 + side_2 + side_3 + side_4
    print("Perimeter of trapezoid:", perimeter_of_trapezoid)

def main():
    while True:  
        print("\nAvailable shapes: [square, rectangle, triangle, circle, parallelogram, rhombus, trapezoid]")
        choice = input("Out of the above options, which shape's perimeter do you want to calculate? ").lower()

        if choice == "square":
            square()
        elif choice == "rectangle":
            rectangle()
        elif choice == "triangle":
            triangle()
        elif choice == "circle":
            circle()
        elif choice == "parallelogram":
            parallelogram()
        elif choice == "rhombus":
            rhombus()
        elif choice == "trapezoid":
            trapezoid()
        else:
            print("Invalid choice. Please enter a valid option.")

        repeat = input("Do you want to calculate another perimeter? (yes/no): ").lower()
        if repeat != "yes":
            print("Thank you for using the perimeter calculator! Goodbye.")
            break

if __name__ == "__main__":
    main()
