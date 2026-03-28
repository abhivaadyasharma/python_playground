#Author: Abhivaadya Sharma

import os
import shutil

# Define categories for file extensions
file_categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Documents': ['.txt', '.pdf', '.docx', '.xlsx', '.pptx', '.csv'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
    'Archives': ['.zip', '.tar', '.rar', '.gz'],
    'Code': ['.py', '.html', '.css', '.js'],
    'Others': []  # Files that don't fit into any category
}

# Function to organize files
def organize_files(directory):
    # Change to the specified directory
    os.chdir(directory)

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        # Check if it's a file (not a directory)
        if os.path.isfile(filename):
            # Get file extension
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Find the category for the file
            moved = False
            for category, extensions in file_categories.items():
                if file_extension in extensions:
                    # Create the category folder if it doesn't exist
                    if not os.path.exists(category):
                        os.makedirs(category)
                    
                    # Move the file into the appropriate folder
                    shutil.move(filename, os.path.join(category, filename))
                    print(f"Moved: {filename} -> {category}/")
                    moved = True
                    break
            
            # If no category is found, move it to 'Others'
            if not moved:
                if not os.path.exists('Others'):
                    os.makedirs('Others')
                shutil.move(filename, os.path.join('Others', filename))
                print(f"Moved: {filename} -> Others/")

# Function to get user directory choice
def get_directory_choice():
    print("Select a directory to organize:")
    print("1. Desktop")
    print("2. Downloads")
    print("3. Documents")
    print("4. Custom directory")
    print("5. Exit")

    choice = input("Enter your choice (1-4): ")
    user_directory = ""

    if choice == "1":
        user_directory = os.path.expanduser("~/Desktop")
    elif choice == "2":
        user_directory = os.path.expanduser("~/Downloads")
    elif choice == "3":
        user_directory = os.path.expanduser("~/Documents")
    elif choice == "4":
        user_directory = input("Enter the full path of the directory: ")
    else:
        print("Invalid choice! Please select a valid option.")
        return None

    # Check if the directory exists
    if os.path.isdir(user_directory):
        return user_directory
    else:
        print(f"Directory {user_directory} does not exist. Please try again.")
        return None

# Main program
if __name__ == "__main__":
    directory = get_directory_choice()
    
    if directory:
        organize_files(directory)
