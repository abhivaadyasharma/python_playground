# Author: Abhivaadya Sharma

def area():
    print("Available shapes: [square, rectangle, triangle, circle, parallelogram, rhombus, trapezoid]")
    choice = input("Out of the above options, which shape's area do you want to calculate? ").lower()

    if choice == "square":
        square_area()
    elif choice == "rectangle":
        rectangle_area()
    elif choice == "triangle":
        triangle_area()
    elif choice == "circle":
        circle_area()
    elif choice == "parallelogram":
        parallelogram_area()
    elif choice == "rhombus":
        rhombus_area()
    elif choice == "trapezoid":
        trapezoid_area()
    else:
        print("Invalid choice. Please enter a valid option.")

def square_area():
    sidesq = float(input("Side of square: "))
    areasq = sidesq * sidesq
    print("Area of the square: ", areasq)

def rectangle_area():
    length = float(input("What is length? "))
    breadth = float(input("What is breadth? "))
    area_of_rectangle = length * breadth
    print("Area of rectangle:", area_of_rectangle)

def triangle_area():
    height = float(input("Height: "))
    base = float(input("Base: "))
    area_of_triangle = 0.5 * height * base
    print("Area of triangle:", area_of_triangle)

def circle_area():
    radius = float(input("Radius: "))
    area_of_circle = 3.14159265359 * radius * radius
    print("Area of circle:", area_of_circle)

def parallelogram_area():
    base = float(input("Base: "))
    height = float(input("Height: "))
    area_of_parallelogram = base * height
    print("Area of parallelogram:", area_of_parallelogram)

def rhombus_area():
    diagonal1 = float(input("Length of the first diagonal: "))
    diagonal2 = float(input("Length of the second diagonal: "))
    area_of_rhombus = 0.5 * diagonal1 * diagonal2
    print("Area of rhombus:", area_of_rhombus)

def trapezoid_area():
    base1 = float(input("Length of the first base: "))
    base2 = float(input("Length of the second base: "))
    height = float(input("Height: "))
    area_of_trapezoid = 0.5 * (base1 + base2) * height
    print("Area of trapezoid:", area_of_trapezoid)

def perimeter():
    print("Available shapes: [square, rectangle, triangle, circle, parallelogram, rhombus, trapezoid]")
    choice = input("Out of the above options, which shape's perimeter do you want to calculate? ").lower()

    if choice == "square":
        square_perimeter()
    elif choice == "rectangle":
        rectangle_perimeter()
    elif choice == "triangle":
        triangle_perimeter()
    elif choice == "circle":
        circle_perimeter()
    elif choice == "parallelogram":
        parallelogram_perimeter()
    elif choice == "rhombus":
        rhombus_perimeter()
    elif choice == "trapezoid":
        trapezoid_perimeter()
    else:
        print("Invalid choice. Please enter a valid option.")

def square_perimeter():
    side = float(input("What is the length of side? "))
    perimeter_of_square = 4 * side
    print("Perimeter of square:", perimeter_of_square)

def rectangle_perimeter():
    length = float(input("What is length of rectangle? "))
    breadth = float(input("What is breadth of rectangle? "))
    perimeter_of_rectangle = 2 * (length + breadth)
    print("Perimeter of rectangle:", perimeter_of_rectangle)

def triangle_perimeter():
    side1 = float(input("What is length of First side? ")) 
    side2 = float(input("What is length of Second side? ")) 
    side3 = float(input("What is length of Third side? ")) 
    perimeter_of_triangle = side1 + side2 + side3
    print("Perimeter of triangle:", perimeter_of_triangle)

def circle_perimeter():
    radius = float(input("What is length of radius? ")) 
    perimeter_of_circle = 2 * 3.14159265359 * radius
    print("Perimeter of circle:", perimeter_of_circle)

def parallelogram_perimeter():
    side_1 = float(input("What is the length of the first side? "))
    side_2 = float(input("What is the length of the second side? "))
    perimeter_of_parallelogram = 2 * (side_1 + side_2)
    print("Perimeter of parallelogram:", perimeter_of_parallelogram)

def rhombus_perimeter():
    side = float(input("What is the length of a side? "))
    perimeter_of_rhombus = 4 * side
    print("Perimeter of rhombus:", perimeter_of_rhombus)

def trapezoid_perimeter():
    side_1 = float(input("What is the length of the first side? "))
    side_2 = float(input("What is the length of the second side? "))
    side_3 = float(input("What is the length of the third side? "))
    side_4 = float(input("What is the length of the fourth side? "))
    perimeter_of_trapezoid = side_1 + side_2 + side_3 + side_4
    print("Perimeter of trapezoid:", perimeter_of_trapezoid)

def main():
    while True:
        print("\nAvailable calculations: [perimeter, area]")
        choice = input("Out of the above options, which calculation do you want to perform? ").lower()

        if choice == "perimeter":
            perimeter()
        elif choice == "area":
            area()
        else:
            print("Invalid choice. Please enter a valid option.")

        # Ask if the user wants to make another calculation
        repeat = input("\nDo you want to calculate another area or perimeter? (yes/no): ").lower()
        if repeat != "yes":
            print("Thank you for using the calculator! Goodbye.")
            break  # Exits the while loop

if __name__ == "__main__":
    main()
