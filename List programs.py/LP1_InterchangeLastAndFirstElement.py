#Author: Abhivaadya Sharma

def interchange_elements(my_list):
    if len(my_list) < 2:
        return my_list
    
    my_list[0], my_list[-1] = my_list[-1], my_list[0]
    return my_list

if __name__ == "__main__":
    try:
        input_str = input("Enter list elements separated by space: ")
        my_list = [int(item) for item in input_str.split()]
        
        interchanged_list = interchange_elements(my_list)
        print("List after interchanging first and last elements:", interchanged_list)
    except ValueError:
        print("Invalid input. Please enter integers separated by spaces.")