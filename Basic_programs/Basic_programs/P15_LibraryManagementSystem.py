#Author: Abhivaadya Sharma

import csv
import hashlib
import datetime

# Define the Book class
class Book:
    def __init__(self, title, author, available=True, genre=None, publication_date=None):
        self.title = title
        self.author = author
        self.available = available
        self.genre = genre
        self.publication_date = publication_date  # Added publication date

    def __str__(self):
        return f"'{self.title}' by {self.author} - {'Available' if self.available else 'Not Available'}"

    def get_book_info(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nGenre: {self.genre}\nPublication Date: {self.publication_date}\n{'Available' if self.available else 'Not Available'}"

    def is_overdue(self, borrow_date):
        # Check if the book is overdue based on a borrow date
        due_date = borrow_date + datetime.timedelta(days=14)  # Assume books are due after 14 days
        return datetime.datetime.now() > due_date


# Define the User class
class User:
    def __init__(self, username, password, role="user", approved=False):
        self.username = username
        self.password = password
        self.role = role  # user or admin
        self.approved = approved  # Whether the user is approved to borrow books
        self.borrowed_books = []
        self.borrow_limit = 5  # Max 5 books per user
        self.borrowed_genres = {}  # Genre-based borrow tracking

    def __str__(self):
        return f"User {self.username} ({'Admin' if self.role == 'admin' else 'User'})"

    def borrow_book(self, book):
        if book.available and self.can_borrow(book):
            self.borrowed_books.append(book)
            book.available = False
            self.borrowed_genres[book.genre] = self.borrowed_genres.get(book.genre, 0) + 1
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.available = True
            self.borrowed_genres[book.genre] -= 1
            if self.borrowed_genres[book.genre] == 0:
                del self.borrowed_genres[book.genre]
            return True
        return False

    def can_borrow(self, book):
        if len(self.borrowed_books) >= self.borrow_limit:
            print(f"You cannot borrow more than {self.borrow_limit} books.")
            return False
        if book.genre and self.borrowed_genres.get(book.genre, 0) >= 3:
            print(f"You have already borrowed the maximum of 3 {book.genre} books.")
            return False
        return True

    def view_borrowed_books(self):
        if self.borrowed_books:
            print("Books you have borrowed:")
            for book in self.borrowed_books:
                print(f"- {book.title} by {book.author}")
        else:
            print("You haven't borrowed any books.")

    def has_overdue_books(self):
        for book in self.borrowed_books:
            # Here you can calculate overdue books if we had borrow date tracking
            print(f"Checking overdue for {book.title}")
            # Placeholder to demonstrate the overdue feature
            pass


# Helper Functions for Book Management
def add_book(book_list, title, author, genre=None, publication_date=None):
    # Avoid duplicate books (same title and author)
    if any(book.title.lower() == title.lower() and book.author.lower() == author.lower() for book in book_list):
        print(f"The book '{title}' by {author} is already in the system.")
        return
    book = Book(title, author, genre=genre, publication_date=publication_date)
    book_list.append(book)
    save_books_to_csv(book_list)
    print(f"Book '{title}' by {author} added successfully.")

def view_books(book_list):
    if not book_list:
        print("No books available.")
        return

    print("List of books:")
    for book in book_list:
        print(book)

def search_books(book_list, search_term):
    search_term = search_term.lower()
    results = [book for book in book_list if search_term in book.title.lower() or search_term in book.author.lower()]
    if results:
        print("Search results:")
        for book in results:
            print(book)
    else:
        print("No books found.")

def delete_book(book_list, title, author):
    book_to_delete = next((book for book in book_list if book.title.lower() == title.lower() and book.author.lower() == author.lower()), None)
    if book_to_delete:
        book_list.remove(book_to_delete)
        save_books_to_csv(book_list)
        print(f"Book '{title}' by {author} deleted.")
    else:
        print(f"Book '{title}' by {author} not found.")

def display_overdue_books(user):
    overdue_books = [book for book in user.borrowed_books if book.is_overdue(book.borrow_date)]
    if overdue_books:
        print("You have overdue books:")
        for book in overdue_books:
            print(book)
    else:
        print("No overdue books.")


# User and Admin authentication functions using SHA-256
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))  # Convert password to bytes
    return sha256.hexdigest()  # Return hashed password

def verify_password(stored_hash, password):
    return stored_hash == hash_password(password)  # Check if the hash matches

def register_user(users_list, username, password, role="user"):
    if any(user.username == username for user in users_list):
        print("Username already exists. Try a different one.")
        return
    if len(password) < 6:
        print("Password should be at least 6 characters long.")
        return
    hashed_password = hash_password(password)  # Use new SHA-256 function
    new_user = User(username, hashed_password, role)
    users_list.append(new_user)
    save_users_to_csv(users_list)
    print(f"User '{username}' registered successfully.")

def authenticate_user(users_list, username, password):
    for user in users_list:
        if user.username == username and verify_password(user.password, password):  # Use SHA-256 verification
            return user
    print("Invalid username or password.")
    return None


# CSV Functions for loading and saving data
def load_books_from_csv():
    books = []
    try:
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                title, author, available, genre, publication_date = row
                books.append(Book(title, author, available == 'True', genre, publication_date))
    except FileNotFoundError:
        pass
    return books

def save_books_to_csv(book_list):
    with open('books.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Available', 'Genre', 'Publication Date'])
        for book in book_list:
            writer.writerow([book.title, book.author, book.available, book.genre, book.publication_date])

def load_users_from_csv():
    users = []
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                username, password, role = row
                users.append(User(username, password, role))
    except FileNotFoundError:
        pass
    return users

def save_users_to_csv(users_list):
    with open('users.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password', 'Role'])
        for user in users_list:
            writer.writerow([user.username, user.password, user.role])


# Audit Log
def log_action(action, username):
    with open("audit_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {username}: {action}\n")


# Input validation helper function
def get_input(prompt, valid_func=None, error_message="Invalid input. Please try again."):
    while True:
        user_input = input(prompt)
        if valid_func and not valid_func(user_input):
            print(error_message)
        else:
            return user_input


# Menu for User Operations (for regular users)
def user_menu(user, books):
    while True:
        print("\n1. View Books")
        print("2. Search Books")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. View Borrowed Books")
        print("6. Logout")
        print("7. View Overdue Books")  # New feature to show overdue books

        choice = get_input("Enter your choice: ", valid_func=lambda x: x in '1234567')

        if choice == '1':
            view_books(books)

        elif choice == '2':
            search_term = input("Enter title or author to search: ")
            search_books(books, search_term)

        elif choice == '3':
            if user.can_borrow():
                title = input("Enter title of the book you want to borrow: ")
                book_to_borrow = next((book for book in books if book.title.lower() == title.lower()), None)
                if book_to_borrow and user.borrow_book(book_to_borrow):
                    print(f"You have borrowed '{book_to_borrow.title}'.")
                    log_action(f"Borrowed '{book_to_borrow.title}'", user.username)
                else:
                    print("Book not available or already borrowed.")
            else:
                print("You cannot borrow more than 5 books.")

        elif choice == '4':
            title = input("Enter title of the book you want to return: ")
            book_to_return = next((book for book in user.borrowed_books if book.title.lower() == title.lower()), None)
            if book_to_return and user.return_book(book_to_return):
                print(f"You have returned '{book_to_return.title}'.")
                log_action(f"Returned '{book_to_return.title}'", user.username)
            else:
                print("You haven't borrowed this book.")

        elif choice == '5':
            user.view_borrowed_books()

        elif choice == '6':
            print("Logging out...")
            break

        elif choice == '7':
            display_overdue_books(user)

        else:
            print("Invalid choice, please try again.")


# Menu for Admin Operations
def admin_menu(user, users, books, pending_requests):
    while True:
        print("\n1. View Books")
        print("2. Search Books")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. View Borrowed Books")
        print("6. Logout")
        print("7. Admin: Add Book")
        print("8. Admin: Delete Book")
        print("9. Admin: Change User Role")
        print("10. Admin: Approve User Requests")
        print("11. Admin: View All Users and Borrowed Books")

        choice = get_input("Enter your choice: ", valid_func=lambda x: x in '1234567891011')

        if choice == '1':
            view_books(books)

        elif choice == '2':
            search_term = input("Enter title or author to search: ")
            search_books(books, search_term)

        elif choice == '3':
            if user.can_borrow():
                title = input("Enter title of the book you want to borrow: ")
                book_to_borrow = next((book for book in books if book.title.lower() == title.lower()), None)
                if book_to_borrow and user.borrow_book(book_to_borrow):
                    print(f"You have borrowed '{book_to_borrow.title}'.")
                    log_action(f"Borrowed '{book_to_borrow.title}'", user.username)
                else:
                    print("Book not available or already borrowed.")
            else:
                print("You cannot borrow more than 5 books.")

        elif choice == '4':
            title = input("Enter title of the book you want to return: ")
            book_to_return = next((book for book in user.borrowed_books if book.title.lower() == title.lower()), None)
            if book_to_return and user.return_book(book_to_return):
                print(f"You have returned '{book_to_return.title}'.")
                log_action(f"Returned '{book_to_return.title}'", user.username)
            else:
                print("You haven't borrowed this book.")

        elif choice == '5':
            user.view_borrowed_books()

        elif choice == '6':
            print("Logging out...")
            break

        elif choice == '7':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre (optional): ")
            publication_date = input("Enter publication date (optional - YYYY-MM-DD): ")
            add_book(books, title, author, genre, publication_date)

        elif choice == '8':
            title = input("Enter title of the book to delete: ")
            author = input("Enter author of the book to delete: ")
            delete_book(books, title, author)

        elif choice == '9':
            target_username = input("Enter username to change role: ")
            new_role = input("Enter new role (user/admin): ").lower()
            user_to_modify = next((user for user in users if user.username == target_username), None)
            if user_to_modify:
                if new_role in ['user', 'admin']:
                    user_to_modify.role = new_role
                    save_users_to_csv(users)
                    print(f"User '{target_username}' role changed to {new_role}.")
                    log_action(f"Changed role of '{target_username}' to {new_role}", user.username)
                else:
                    print("Invalid role. Must be 'user' or 'admin'.")
            else:
                print(f"User '{target_username}' not found.")

        elif choice == '10':
            print("Pending User Requests:")
            for request in pending_requests:
                print(request)

            target_username = input("Enter username to approve or reject: ")
            action = input("Approve (Y/N): ").strip().lower()

            user_to_approve = next((user for user in pending_requests if user.username == target_username), None)

            if user_to_approve:
                if action == 'y':
                    user_to_approve.role = 'user'
                    user_to_approve.approved = True
                    users.append(user_to_approve)
                    pending_requests.remove(user_to_approve)
                    save_users_to_csv(users)
                    print(f"User '{target_username}' is now approved and granted user role.")
                elif action == 'n':
                    pending_requests.remove(user_to_approve)
                    print(f"Request for '{target_username}' has been rejected.")
                else:
                    print("Invalid choice.")
            else:
                print(f"User '{target_username}' not found in requests.")

        elif choice == '11':
            print("All Users and Borrowed Books:")
            for u in users:
                print(f"User: {u.username} (Role: {u.role})")
                u.view_borrowed_books()

        else:
            print("Invalid choice, please try again.")


# Main program loop
def main():
    books = load_books_from_csv()
    users = load_users_from_csv()

    pending_requests = []  # List to store user requests

    print("Welcome to the Library Management System")

    if not users:
        print("No users registered. The first user will be an admin.")

    logged_in_user = None

    while True:
        print("\n1. Register")
        print("2. Login (User/Admin)")
        print("3. Exit")

        choice = get_input("Enter your choice: ", valid_func=lambda x: x in '123')

        if choice == '1':
            if len(users) == 0:
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                register_user(users, username, password, role="admin")
            else:
                # Allow people to request for being users
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                register_user(users, username, password, role="user")
                pending_requests.append(User(username, hash_password(password), role="user"))

                print("Your request to be a user has been submitted for approval.")
        
        elif choice == '2':
            if logged_in_user:
                print(f"Already logged in as {logged_in_user.username}")
                continue

            username = input("Enter username: ")
            password = input("Enter password: ")
            logged_in_user = authenticate_user(users, username, password)
            
            if logged_in_user:
                print(f"Welcome, {logged_in_user.username}!")
                if logged_in_user.role == "admin":
                    admin_menu(logged_in_user, users, books, pending_requests)
                else:
                    user_menu(logged_in_user, books)

        elif choice == '3':
            print("Exiting system.")
            break 
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
