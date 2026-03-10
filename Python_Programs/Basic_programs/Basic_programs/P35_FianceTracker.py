import sqlite3
import bcrypt
import re
import getpass
import os
import csv
from datetime import datetime
from colorama import Fore, Style, init

# Initialize Colorama for terminal colors
init(autoreset=True)

# -----------------------------
# Configuration & Database
# -----------------------------
DB_NAME = "finance_app.db"
INCOME = "Income"
EXPENSE = "Expense"

class FinanceDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_tables()

    def query(self, sql, params=(), commit=False, fetch=False):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if commit:
                conn.commit()
            return cursor.fetchall() if fetch else cursor.lastrowid

    def create_tables(self):
        # Users Table
        self.query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                security_question TEXT NOT NULL,
                security_answer BLOB NOT NULL
            )
        """, commit=True)

        # Transactions Table
        self.query("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                type TEXT,
                category TEXT,
                amount REAL CHECK(amount>=0),
                note TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """, commit=True)

        # Budgets Table
        self.query("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                monthly_limit REAL CHECK(monthly_limit>=0),
                UNIQUE(user_id, category),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """, commit=True)

        # Goals Table
        self.query("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                goal_name TEXT,
                target_amount REAL CHECK(target_amount>0),
                current_saved REAL DEFAULT 0,
                UNIQUE(user_id, goal_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """, commit=True)

db = FinanceDB(DB_NAME)

# -----------------------------
# Utility Helpers
# -----------------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_strong_password(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))

def get_input(prompt, required=True):
    val = input(prompt).strip()
    if not val and required:
        print(Fore.RED + "⚠ Field cannot be empty.")
        return get_input(prompt, required)
    return val

def get_available_balance(user_id):
    """Calculates balance minus what is already committed to goals."""
    income = db.query("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type=?", (user_id, INCOME), fetch=True)[0][0] or 0
    expense = db.query("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type=?", (user_id, EXPENSE), fetch=True)[0][0] or 0
    locked_in_goals = db.query("SELECT SUM(current_saved) FROM goals WHERE user_id=?", (user_id,), fetch=True)[0][0] or 0
    return income - expense - locked_in_goals

# -----------------------------
# Auth & Recovery
# -----------------------------

def register():
    username = get_input("New username: ").lower()
    password = getpass.getpass("New password: ")
    
    if not is_strong_password(password):
        print(Fore.RED + "⚠ Weak password! (Min 8 chars, 1 Uppercase, 1 Number)")
        input("Press Enter...")
        return

    question = get_input("Security Question: ")
    answer = getpass.getpass("Answer: ").lower()

    try:
        db.query("""INSERT INTO users (username, password, security_question, security_answer) 
                 VALUES (?, ?, ?, ?)""", 
                 (username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()), 
                  question, bcrypt.hashpw(answer.encode(), bcrypt.gensalt())), commit=True)
        print(Fore.GREEN + "✔ Account created!")
    except sqlite3.IntegrityError:
        print(Fore.RED + "⚠ Username already exists.")
    input("Press Enter...")

def login():
    username = get_input("Username: ").lower()
    password = getpass.getpass("Password: ")
    
    user = db.query("SELECT id, password FROM users WHERE username=?", (username,), fetch=True)
    
    if user and bcrypt.checkpw(password.encode(), user[0][1]):
        print(Fore.GREEN + "✔ Login successful!")
        return user[0][0]
    
    print(Fore.RED + "⚠ Access denied.")
    input("Press Enter...")
    return None

def recover_password():
    username = get_input("Enter username for recovery: ").lower()
    user_data = db.query("SELECT security_question, security_answer FROM users WHERE username=?", (username,), fetch=True)

    if not user_data:
        print(Fore.RED + "⚠ User not found.")
        input("Press Enter...")
        return

    question, hashed_answer = user_data[0]
    print(f"\nSecurity Question: {Fore.CYAN}{question}")
    answer_attempt = getpass.getpass("Your Answer: ").lower()

    if bcrypt.checkpw(answer_attempt.encode(), hashed_answer):
        print(Fore.GREEN + "✔ Identity verified!")
        new_password = getpass.getpass("Enter new password: ")
        
        if is_strong_password(new_password):
            new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            db.query("UPDATE users SET password=? WHERE username=?", (new_hash, username), commit=True)
            print(Fore.GREEN + "✔ Password updated successfully!")
        else:
            print(Fore.RED + "⚠ Password too weak.")
    else:
        print(Fore.RED + "⚠ Incorrect answer.")
    input("Press Enter...")

# -----------------------------
# Savings Goal Logic
# -----------------------------

def manage_goals(user_id):
    while True:
        clear_screen()
        print(Fore.CYAN + "=== SAVINGS GOALS ===")
        goals = db.query("SELECT goal_name, target_amount, current_saved FROM goals WHERE user_id=?", (user_id,), fetch=True)
        
        if not goals:
            print("No goals set yet.")
        else:
            for name, target, saved in goals:
                perc = min((saved / target) * 100, 100)
                bar_len = 20
                filled = int((perc/100) * bar_len)
                bar = "█" * filled + "-" * (bar_len - filled)
                print(f"\nGoal: {Fore.YELLOW}{name}")
                print(f"Progress: |{bar}| {perc:.1f}% (${saved:,.2f} / ${target:,.2f})")

        print("\n1) New Goal  2) Transfer to Goal  3) Withdraw from Goal  4) Delete Goal  5) Back")
        choice = input("\nChoice: ")
        
        if choice == "1":
            name = get_input("Goal Name: ").title()
            try:
                target = float(get_input("Target Amount: "))
                db.query("INSERT INTO goals (user_id, goal_name, target_amount) VALUES (?,?,?)", (user_id, name, target), commit=True)
                print(Fore.GREEN + "Goal Created!")
            except: print(Fore.RED + "Invalid amount.")
            
        elif choice == "2":
            available = get_available_balance(user_id)
            print(f"\nAvailable to Transfer: {Fore.GREEN}${available:,.2f}")
            g_name = get_input("Goal Name: ").title()
            try:
                amt = float(get_input("Amount to save: "))
                if amt <= available:
                    db.query("UPDATE goals SET current_saved = current_saved + ? WHERE user_id=? AND goal_name=?", (amt, user_id, g_name), commit=True)
                    print(Fore.GREEN + "Transfer successful!")
                else: print(Fore.RED + "Insufficient balance.")
            except: print(Fore.RED + "Error processing transfer.")
            
        elif choice == "3":
            g_name = get_input("Goal Name: ").title()
            res = db.query("SELECT current_saved FROM goals WHERE user_id=? AND goal_name=?", (user_id, g_name), fetch=True)
            if res:
                saved = res[0][0]
                print(f"Currently saved in {g_name}: {Fore.YELLOW}${saved:,.2f}")
                try:
                    amt = float(get_input("Amount to withdraw: "))
                    if amt <= saved:
                        db.query("UPDATE goals SET current_saved = current_saved - ? WHERE user_id=? AND goal_name=?", (amt, user_id, g_name), commit=True)
                        print(Fore.GREEN + f"${amt} moved back to Main Balance.")
                    else: print(Fore.RED + "Cannot withdraw more than saved.")
                except: print(Fore.RED + "Invalid input.")
            else: print(Fore.RED + "Goal not found.")

        elif choice == "4":
            g_name = get_input("Goal Name to Delete: ").title()
            db.query("DELETE FROM goals WHERE user_id=? AND goal_name=?", (user_id, g_name), commit=True)
            print(Fore.YELLOW + "Goal deleted.")

        elif choice == "5": break
        input("\nPress Enter...")

# -----------------------------
# Finance Logic
# -----------------------------

def add_transaction(user_id, t_type):
    print(f"\n--- Add {t_type} ---")
    category = get_input("Category: ").title()
    try:
        amount = float(get_input("Amount: "))
    except ValueError:
        print(Fore.RED + "⚠ Numbers only.")
        return

    note = input("Note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.query("INSERT INTO transactions (user_id, date, type, category, amount, note) VALUES (?,?,?,?,?,?)",
             (user_id, date, t_type, category, amount, note), commit=True)
    
    if t_type == EXPENSE:
        check_budget(user_id, category)
    
    print(Fore.GREEN + f"✔ Recorded.")
    input("Press Enter...")

def check_budget(user_id, category):
    month = datetime.now().strftime("%Y-%m")
    spent = db.query("""SELECT SUM(amount) FROM transactions 
                     WHERE user_id=? AND category=? AND type='Expense' AND strftime('%Y-%m', date)=?""",
                     (user_id, category, month), fetch=True)[0][0] or 0
    
    budget = db.query("SELECT monthly_limit FROM budgets WHERE user_id=? AND category=?", 
                      (user_id, category), fetch=True)
    
    if budget:
        limit = budget[0][0]
        perc = (spent / limit) * 100
        print(f"\nBudget Status for {category}: {spent:.2f} / {limit:.2f} ({perc:.1f}%)")
        if spent > limit:
            print(Fore.RED + "‼ BUDGET EXCEEDED!")
        elif perc > 80:
            print(Fore.YELLOW + "⚠ Over 80% used.")

def view_total_balance(user_id):
    total_income = db.query("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type=?", (user_id, INCOME), fetch=True)[0][0] or 0
    total_expense = db.query("SELECT SUM(amount) FROM transactions WHERE user_id=? AND type=?", (user_id, EXPENSE), fetch=True)[0][0] or 0
    goal_savings = db.query("SELECT SUM(current_saved) FROM goals WHERE user_id=?", (user_id,), fetch=True)[0][0] or 0
    
    available = total_income - total_expense - goal_savings
    
    print(f"\n{Fore.CYAN}--- Financial Snapshot ---")
    print(f"Total Income      : {Fore.GREEN}{total_income:,.2f}")
    print(f"Total Expense     : {Fore.RED}{total_expense:,.2f}")
    print(f"Locked in Goals   : {Fore.YELLOW}{goal_savings:,.2f}")
    print("-" * 35)
    
    balance_color = Fore.GREEN if available >= 0 else Fore.RED
    print(f"Available Balance : {balance_color}{available:,.2f}")
    input("\nPress Enter to return...")

def view_all_transactions(user_id):
    rows = db.query("SELECT date, type, category, amount, note FROM transactions WHERE user_id=? ORDER BY date DESC", 
                    (user_id,), fetch=True)
    
    print(f"\n{'Date':<20} | {'Type':<8} | {'Category':<15} | {'Amount':<10} | {'Note'}")
    print("-" * 85)
    for r in rows:
        color = Fore.GREEN if r[1] == INCOME else Fore.RED
        print(f"{r[0][:16]:<20} | {color}{r[1]:<8}{Style.RESET_ALL} | {r[2]:<15} | {r[3]:<10.2f} | {r[4]}")
    input("\nPress Enter to return...")

def monthly_report(user_id):
    month = datetime.now().strftime("%Y-%m")
    print(f"\n--- Monthly Summary: {month} ---")
    
    summary = db.query("""SELECT category, SUM(amount) FROM transactions 
                       WHERE user_id=? AND type='Expense' AND strftime('%Y-%m', date)=?
                       GROUP BY category""", (user_id, month), fetch=True)
    
    if not summary:
        print("No expenses logged for this month.")
    else:
        for cat, total in summary:
            print(f"{cat:<15}: ${total:>10.2f}")
    input("\nPress Enter...")

# -----------------------------
# Main Menus
# -----------------------------

def user_menu(user_id):
    while True:
        clear_screen()
        print(Fore.CYAN + "=== USER DASHBOARD ===")
        print("1) Add Income")
        print("2) Add Expense")
        print("3) View History")
        print("4) Savings Goals (New)")
        print("5) Set Budget")
        print("6) Monthly Summary")
        print("7) Total Balance")
        print("8) Logout")
        
        choice = input("\nChoice: ")
        
        if choice == "1": add_transaction(user_id, INCOME)
        elif choice == "2": add_transaction(user_id, EXPENSE)
        elif choice == "3": view_all_transactions(user_id)
        elif choice == "4": manage_goals(user_id)
        elif choice == "5":
            cat = get_input("Category: ").title()
            try:
                limit = float(get_input("Monthly Limit: "))
                db.query("INSERT OR REPLACE INTO budgets (user_id, category, monthly_limit) VALUES (?,?,?)",
                         (user_id, cat, limit), commit=True)
                print(Fore.GREEN + "Budget updated.")
            except ValueError:
                print(Fore.RED + "Invalid number.")
            input("Press Enter...")
        elif choice == "6": monthly_report(user_id)
        elif choice == "7": view_total_balance(user_id)
        elif choice == "8": break

def main():
    while True:
        clear_screen()
        print(Fore.YELLOW + "------KernelFinance Pro--------")
        print("1) Register")
        print("2) Login")
        print("3) Recover Password")
        print("4) Exit")
        
        choice = input("\nChoice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            uid = login()
            if uid:
                user_menu(uid)
        elif choice == "3":
            recover_password()
        elif choice == "4":
            print(Fore.GREEN + "Goodbye!")
            break

if __name__ == "__main__":
    main()