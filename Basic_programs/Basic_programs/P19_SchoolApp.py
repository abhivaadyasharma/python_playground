import sqlite3
import csv

DB_NAME = 'students.db'

# ---------------------- Database Setup ----------------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_class TEXT NOT NULL,
                father_name TEXT NOT NULL,
                father_phone TEXT NOT NULL,
                marks INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# ---------------------- Core Operations ----------------------
def add_student():
    name = input("👤 Enter student's name: ").strip()
    student_class = input("🏫 Enter class: ").strip()
    father_name = input("👨 Enter father's name: ").strip()
    father_phone = input("📞 Enter father's phone number: ").strip()

    if not (name and student_class and father_name and father_phone):
        print("❌ All fields are required.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, student_class, father_name, father_phone) VALUES (?, ?, ?, ?)",
            (name, student_class, father_name, father_phone)
        )
        conn.commit()
        print("✅ Student added successfully!\n")

def view_students():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

    if rows:
        print("\n📋 Student List:")
        print(f"{'ID':<5} {'Name':<20} {'Class':<10} {'Father Name':<20} {'Father Phone':<15} {'Marks':<6}")
        print("-" * 85)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<20} {row[4]:<15} {row[5]:<6}")
    else:
        print("⚠️ No students found.\n")

def update_student():
    try:
        sid = int(input("🔁 Enter student ID to update: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    name = input("👤 New name: ").strip()
    student_class = input("🏫 New class: ").strip()
    father_name = input("👨 New father's name: ").strip()
    father_phone = input("📞 New father's phone number: ").strip()

    if not (name and student_class and father_name and father_phone):
        print("❌ All fields are required.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET name=?, student_class=?, father_name=?, father_phone=? WHERE id=?",
            (name, student_class, father_name, father_phone, sid)
        )
        if cur.rowcount == 0:
            print("⚠️ No student found with that ID.\n")
        else:
            conn.commit()
            print("✅ Student updated successfully!\n")

def delete_student():
    try:
        sid = int(input("🗑️ Enter student ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (sid,))
        if cur.rowcount == 0:
            print("⚠️ No student found with that ID.\n")
        else:
            conn.commit()
            print("🗑️ Student deleted successfully!\n")

# ---------------------- Marks Operations ----------------------
def add_update_marks():
    try:
        sid = int(input("🔢 Enter student ID to add/update marks: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    try:
        marks = int(input("📊 Enter marks (0-100): "))
        if marks < 0 or marks > 100:
            print("❌ Marks should be between 0 and 100.")
            return
    except ValueError:
        print("❌ Marks must be a number.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE students SET marks=? WHERE id=?", (marks, sid))
        if cur.rowcount == 0:
            print("⚠️ No student found with that ID.\n")
        else:
            conn.commit()
            print("✅ Marks updated successfully!\n")

def top_students():
    n = input("🔝 How many top students to display (by marks)? ").strip()
    try:
        n = int(n)
        if n <= 0:
            print("❌ Number must be positive.")
            return
    except ValueError:
        print("❌ Invalid number.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY marks DESC LIMIT ?", (n,))
        rows = cur.fetchall()

    if rows:
        print(f"\n🏅 Top {n} Students by Marks:")
        print(f"{'ID':<5} {'Name':<20} {'Class':<10} {'Father Name':<20} {'Father Phone':<15} {'Marks':<6}")
        print("-" * 85)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<20} {row[4]:<15} {row[5]:<6}")
    else:
        print("⚠️ No students found.\n")

# ---------------------- Optional Features ----------------------
def search_students():
    term = input("🔍 Enter search term (name/class/father's name): ").strip()
    if not term:
        print("❌ Search term cannot be empty.")
        return
    like_term = f"%{term}%"
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ? OR student_class LIKE ? OR father_name LIKE ?",
            (like_term, like_term, like_term)
        )
        rows = cur.fetchall()

    if rows:
        print("\n🔎 Search Results:")
        print(f"{'ID':<5} {'Name':<20} {'Class':<10} {'Father Name':<20} {'Father Phone':<15} {'Marks':<6}")
        print("-" * 85)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<20} {row[4]:<15} {row[5]:<6}")
    else:
        print("⚠️ No matching students found.\n")

def export_to_csv():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

    if not rows:
        print("⚠️ No data to export.\n")
        return

    filename = input("💾 Enter filename to export (e.g., students.csv): ").strip()
    if not filename:
        print("❌ Filename cannot be empty.")
        return
    if not filename.endswith('.csv'):
        filename += '.csv'

    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Class', 'Father Name', 'Father Phone', 'Marks'])
            writer.writerows(rows)
        print(f"✅ Data exported successfully to {filename}\n")
    except Exception as e:
        print(f"❌ Error writing file: {e}")

# ---------------------- Menu System ----------------------
def main_menu():
    while True:
        print("\n📘 STUDENT MANAGEMENT SYSTEM")
        print("1️⃣ Add Student")
        print("2️⃣ View Students")
        print("3️⃣ Update Student")
        print("4️⃣ Delete Student")
        print("5️⃣ Search Students")
        print("6️⃣ Export to CSV")
        print("7️⃣ Add/Update Student Marks")
        print("8️⃣ Top Students by Marks")
        print("9️⃣ Exit")

        choice = input("👉 Enter your choice (1–9): ").strip()

        match choice:
            case '1':
                add_student()
            case '2':
                view_students()
            case '3':
                update_student()
            case '4':
                delete_student()
            case '5':
                search_students()
            case '6':
                export_to_csv()
            case '7':
                add_update_marks()
            case '8':
                top_students()
            case '9':
                print("👋 Exiting program. Goodbye!")
                break
            case _:
                print("❌ Invalid choice. Please try again.\n")

# ---------------------- Entry Point ----------------------
if __name__ == "__main__":
    init_db()
    main_menu()
