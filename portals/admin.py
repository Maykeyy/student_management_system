# portals/admin.py:
from utils import Display
from models.user import Admin
from models.course import Course

class AdminPortal:
    def __init__(self, user):
        self.user = user
        self.display = Display()

    def show_menu(self):
        while True:
            self.display.header("ADMIN PORTAL")
            self.display.menu([
                "Manage Teachers",
                "Manage Students", 
                "Manage Courses"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.manage_teachers()
            elif choice == '2':
                self.manage_students()
            elif choice == '3':
                self.manage_courses()
            elif choice == '0':
                break

    # --- Teacher Management ---
    def manage_teachers(self):
        while True:
            self.display.header("TEACHER MANAGEMENT")
            self.display.menu([
                "View Teachers",
                "Add Teacher",
                "Update Teacher",
                "Delete Teacher"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_teachers()
            elif choice == '2':
                self.add_teacher()
            elif choice == '3':
                self.update_teacher()
            elif choice == '4':
                self.delete_teacher()
            elif choice == '0':
                break

    def view_teachers(self):
        teachers = Admin.get_teachers()
        if teachers:
            self.display.table_header(["ID", "User ID", "Name", "Email", "Position"])
            for t in teachers:
                self.display.table_row([t[0], t[1], t[2], t[3], t[4] or "N/A"])
        else:
            self.display.info("No teachers found")
        input("\nPress Enter to continue...")

    def add_teacher(self):
        name = input("Teacher Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        email = input("Email: ")
        if not email:
            self.display.info("Operation cancelled.")
            return
        password = input("Password: ")
        if not password:
            self.display.info("Operation cancelled.")
            return
        position = input("Position: ")
        if not position:
            self.display.info("Operation cancelled.")
            return
        
        result = Admin.create_teacher(name, email, password, position)
        if result:
            self.display.success("Teacher added successfully!")
        else:
            self.display.error("Failed to add teacher")
        input("\nPress Enter to continue...")

    def update_teacher(self):
        self.view_teachers()
        user_id = input("Enter Teacher User ID (6 digits) to update: ")
        if not user_id:
            self.display.info("Operation cancelled.")
            return
        if len(user_id) != 6 or not user_id.isdigit():
            self.display.error("Invalid User ID. Please enter a 6-digit Teacher User ID.")
            input("\nPress Enter to continue...")
            return
        name = input("New Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        email = input("New Email: ")
        if not email:
            self.display.info("Operation cancelled.")
            return
        password = input("New Password: ")
        if not password:
            self.display.info("Operation cancelled.")
            return
        position = input("New Position: ")
        if not position:
            self.display.info("Operation cancelled.")
            return
        
        result = Admin.update_teacher(user_id, name, email, password, position)
        if result is not None:
            self.display.success("Teacher updated successfully!")
        else:
            self.display.error("Failed to update teacher")
        input("\nPress Enter to continue...")

    def delete_teacher(self):
        self.view_teachers()
        user_id = input("Enter Teacher User ID (6 digits) to delete: ")
        if len(user_id) != 6 or not user_id.isdigit():
            self.display.error("Invalid User ID. Please enter a 6-digit Teacher User ID.")
            input("\nPress Enter to continue...")
            return
        result = Admin.delete_teacher(user_id)
        if result is not None:
            self.display.success("Teacher deleted successfully!")
        else:
            self.display.error("Failed to delete teacher")
        input("\nPress Enter to continue...")

    # --- Student Management ---
    def manage_students(self):
        while True:
            self.display.header("STUDENT MANAGEMENT")
            self.display.menu([
                "View Students",
                "Add Student",
                "Update Student",
                "Delete Student"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_students()
            elif choice == '2':
                self.add_student()
            elif choice == '3':
                self.update_student()
            elif choice == '4':
                self.delete_student()
            elif choice == '0':
                break

    def view_students(self):
        students = Admin.get_students()
        if students:
            self.display.table_header(["ID", "User ID", "Name", "Email", "Course", "Year"])
            for s in students:
                self.display.table_row([s[0], s[1], s[2], s[3], s[4] or "N/A", s[5]])
        else:
            self.display.info("No students found")
        input("\nPress Enter to continue...")

    def add_student(self):
        self.view_courses()
        name = input("Student Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        email = input("Email: ")
        if not email:
            self.display.info("Operation cancelled.")
            return
        password = input("Password: ")
        if not password:
            self.display.info("Operation cancelled.")
            return
        course_id = input("Course ID: ")
        if not course_id:
            self.display.info("Operation cancelled.")
            return
        year_level = input("Year Level: ")
        if not year_level:
            self.display.info("Operation cancelled.")
            return
        
        result = Admin.create_student(name, email, password, course_id, year_level)
        if result:
            self.display.success("Student added successfully!")
        else:
            self.display.error("Failed to add student")
        input("\nPress Enter to continue...")

    def update_student(self):
        self.view_students()
        user_id = input("Enter Student User ID (6 digits) to update: ")
        if not user_id:
            self.display.info("Operation cancelled.")
            return
        if len(user_id) != 6 or not user_id.isdigit():
            self.display.error("Invalid User ID. Please enter a 6-digit Student User ID.")
            input("\nPress Enter to continue...")
            return
        name = input("New Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        email = input("New Email: ")
        if not email:
            self.display.info("Operation cancelled.")
            return
        password = input("New Password: ")
        if not password:
            self.display.info("Operation cancelled.")
            return
        course_id = input("New Course ID: ")
        if not course_id:
            self.display.info("Operation cancelled.")
            return
        year_level = input("New Year Level: ")
        if not year_level:
            self.display.info("Operation cancelled.")
            return
        
        result = Admin.update_student(user_id, name, email, password, course_id, year_level)
        if result is not None:
            self.display.success("Student updated successfully!")
        else:
            self.display.error("Failed to update student")
        input("\nPress Enter to continue...")

    def delete_student(self):
        self.view_students()
        user_id = input("Enter Student User ID (6 digits) to delete: ")
        if len(user_id) != 6 or not user_id.isdigit():
            self.display.error("Invalid User ID. Please enter a 6-digit Student User ID.")
            input("\nPress Enter to continue...")
            return
        result = Admin.delete_student(user_id)
        if result is not None:
            self.display.success("Student deleted successfully!")
        else:
            self.display.error("Failed to delete student")
        input("\nPress Enter to continue...")

    # --- Course Management ---
    def manage_courses(self):
        while True:
            self.display.header("COURSE MANAGEMENT")
            self.display.menu([
                "View Courses",
                "Add Course",
                "Update Course",
                "Delete Course"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_courses()
            elif choice == '2':
                self.add_course()
            elif choice == '3':
                self.update_course()
            elif choice == '4':
                self.delete_course()
            elif choice == '0':
                break

    def view_courses(self):
        courses = Course.get_all()
        if courses:
            self.display.table_header(["ID", "Name", "Description"])
            for c in courses:
                self.display.table_row([c[0], c[1], c[2] or "N/A"])
        else:
            self.display.info("No courses found")
        input("\nPress Enter to continue...")

    def add_course(self):
        name = input("Course Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        description = input("Description: ")
        if not description:
            self.display.info("Operation cancelled.")
            return
        
        result = Course.create(name, description)
        if result:
            self.display.success("Course added successfully!")
        else:
            self.display.error("Failed to add course")
        input("\nPress Enter to continue...")

    def update_course(self):
        self.view_courses()
        course_id = input("Enter Course ID to update: ")
        if not course_id:
            self.display.info("Operation cancelled.")
            return
        name = input("New Name: ")
        if not name:
            self.display.info("Operation cancelled.")
            return
        description = input("New Description: ")
        if not description:
            self.display.info("Operation cancelled.")
            return
        
        result = Course.update(course_id, name, description)
        if result is not None:
            self.display.success("Course updated successfully!")
        else:
            self.display.error("Failed to update course")
        input("\nPress Enter to continue...")

    def delete_course(self):
        self.view_courses()
        course_id = input("Enter Course ID to delete: ")
        
        result = Course.delete(course_id)
        if result is not None:
            self.display.success("Course deleted successfully!")
        else:
            self.display.error("Failed to delete course")
        input("\nPress Enter to continue...")