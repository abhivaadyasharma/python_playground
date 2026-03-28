#Author:Abhivaadya Sharma

from sympy import symbols, simplify
#Example: Enter variables (comma-separated, e.g., x,y,z): x,y,z,a,b
#         Enter the algebraic expression: x*y + (-11*y*z)*10*a*b/(2*a*b) - 3*x*y*z
#         Simplified expression: x*y - 55*y*z - 3*x*y*z


def algebra_solver():
    print("🔹 Algebraic Expression Solver 🔹")
    print("Supports +, -, *, / between algebraic terms (e.g., x+y, 2*x*y, etc.)")
    print("Example of mixed expression: (x + y)*(x - y) + (x*y)/(x + y)\n")
    
    # Step 1: Get variables from user
    variables = input("Enter variables (comma-separated, e.g., x,y,z): ")
    var_list = symbols(variables.replace(" ", ""))
    
    # Step 2: Get algebraic expression
    expr = input("Enter the algebraic expression: ")
    
    # Step 3: Simplify and show results
    try:
        simplified_expr = simplify(expr)
        print("\n✅ Simplified Expression:")
        print(simplified_expr)
        
    except Exception as e:
        print("\n❌ Error:", e)
        print("Please check your expression syntax!")

# Run the program
if __name__ == "__main__":
    algebra_solver()

