import mysql.connector
import random
import string
import sys

# Database connection config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'student_management'
}

# Utility functions
def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)


def generate_student_id():
    return ''.join(random.choices(string.digits, k=8))


def print_header(title, width=60):
    print("\n" + title.center(width, "="))


def print_menu():
    print_header(" STUDENT MANAGEMENT SYSTEM ")
    options = ["1. Register Student", "2. View Students", "3. Edit Student's Grade", "4. Exit"]
    for opt in options:
        print(opt)


def print_table(headers, rows):
    # compute column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    # header line
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(header_line)
    print(sep_line)
    for row in rows:
        print(" | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))


def register_student():
    conn = get_db_connection()
    cursor = conn.cursor()

    full_name = input("Enter full name: ").strip()
    if not full_name:
        print("Name cannot be empty.")
        return

    cursor.execute("SELECT course_id, course_code FROM courses")
    courses = cursor.fetchall()
    print_table(["ID", "Course"], courses)
    try:
        course_choice = int(input("Select course ID: "))
    except ValueError:
        print("Invalid input.")
        return
    if course_choice not in [c[0] for c in courses]:
        print("Invalid course selection.")
        return

    try:
        year = int(input("Enter year level (1-4): "))
    except ValueError:
        print("Invalid input.")
        return
    if year not in [1, 2, 3, 4]:
        print("Year level must be between 1 and 4.")
        return

    # Generate unique ID
    while True:
        sid = generate_student_id()
        cursor.execute("SELECT 1 FROM students WHERE student_id = %s", (sid,))
        if not cursor.fetchone():
            break

    cursor.execute(
        "INSERT INTO students (student_id, full_name, course_id, year_level) VALUES (%s, %s, %s, %s)",
        (sid, full_name, course_choice, year)
    )
    cursor.execute("INSERT INTO grades (student_id) VALUES (%s)", (sid,))
    conn.commit()
    print(f"Student registered with ID: {sid}")

    cursor.close()
    conn.close()


def view_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("1. Display by course")
    print("2. Display all students")
    choice = input("Choice: ")

    if choice == '1':
        cursor.execute("SELECT course_id, course_code FROM courses")
        courses = cursor.fetchall()
        print_table(["ID", "Course"], courses)
        try:
            c = int(input("Select course ID: "))
        except ValueError:
            print("Invalid input.")
            return
        cursor.execute(
            "SELECT s.student_id, s.full_name, s.year_level, g.quiz, g.activity, g.exam "
            "FROM students s JOIN grades g ON s.student_id=g.student_id WHERE s.course_id=%s", (c,)
        )
        headers = ["ID", "Name", "Year", "Quiz", "Activity", "Exam"]
    else:
        cursor.execute(
            "SELECT s.student_id, s.full_name, c.course_code, s.year_level, g.quiz, g.activity, g.exam "
            "FROM students s "
            "JOIN courses c ON s.course_id=c.course_id "
            "JOIN grades g ON s.student_id=g.student_id"
        )
        headers = ["ID", "Name", "Course", "Year", "Quiz", "Activity", "Exam"]

    rows = cursor.fetchall()
    if rows:
        print_table(headers, rows)
    else:
        print("No students found.")

    cursor.close()
    conn.close()


def edit_grade():
    sid = input("Enter student ID: ").strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM students WHERE student_id = %s", (sid,))
    student = cursor.fetchone()
    if not student:
        print("Student ID not found.")
        return
    print(f"Editing grades for {student[0]} (ID: {sid})")

    try:
        quiz = float(input("Enter new quiz grade: "))
        activity = float(input("Enter new activity grade: "))
        exam = float(input("Enter new exam grade: "))
    except ValueError:
        print("Grades must be numeric.")
        return

    cursor.execute(
        "UPDATE grades SET quiz=%s, activity=%s, exam=%s WHERE student_id=%s",
        (quiz, activity, exam, sid)
    )
    conn.commit()
    print("Grades updated successfully.")

    cursor.close()
    conn.close()


def main():
    while True:
        print_menu()
        choice = input("Select an option: ")

        if choice == '1':
            register_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            edit_grade()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()