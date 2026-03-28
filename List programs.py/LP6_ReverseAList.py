#Author: Abhivaadya Sharma

def get_user_list():
    raw = input("Enter your list items separated by commas: ")
    def convert(x):
        x = x.strip()
        try:
            val = float(x)
            return int(val) if val.is_integer() else val
        except ValueError:
            return x
    return [convert(item) for item in raw.split(",")]

def main():
    user_list = get_user_list()
    if not user_list or user_list == ['']:
        print("List is empty.")
        return

    # Separate numbers and strings
    numbers = [x for x in user_list if isinstance(x, (int, float))]
    strings = [x for x in user_list if isinstance(x, str)]

    print("Choose an operation:")
    print("1. Find maximum")
    print("2. Find minimum")
    print("3. Sort ascending")
    print("4. Sort descending")
    op = input("Enter number of operation: ")

    target_list = numbers if numbers else strings

    if not target_list:
        print("No valid items to operate on.")
        return

    try:
        if op == "1":
            print("Maximum:", max(target_list))
        elif op == "2":
            print("Minimum:", min(target_list))
        elif op == "3":
            print("Sorted ascending:", sorted(target_list))
        elif op == "4":
            print("Sorted descending:", sorted(target_list, reverse=True))
        else:
            print("Invalid operation.")
    except TypeError:
        print("Cannot compare different types in list.")

if __name__ == "__main__":
    main()
