from utils import Display
from models.user import Teacher
from models.subject import Subject
from models.course import Course
from models.enrollment import Enrollment
from models.grade import Grade

class TeacherPortal:
    def __init__(self, user):
        self.user = user
        self.display = Display()
        teacher_data = Teacher.get_by_user_id(user['user_id'])
        self.teacher_id = teacher_data[0] if teacher_data else None

    def show_menu(self):
        while True:
            self.display.header("TEACHER PORTAL")
            self.display.menu([
                "Manage Subjects",
                "Manage Enrollments",
                "Manage Grades"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.manage_subjects()
            elif choice == '2':
                self.manage_enrollments()
            elif choice == '3':
                self.manage_grades()
            elif choice == '0':
                break

    def manage_subjects(self):
        while True:
            self.display.header("SUBJECT MANAGEMENT")
            self.display.menu([
                "View My Subjects",
                "Add Subject",
                "Update Subject",
                "Delete Subject"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_subjects()
            elif choice == '2':
                self.add_subject()
            elif choice == '3':
                self.update_subject()
            elif choice == '4':
                self.delete_subject()
            elif choice == '0':
                break

    def view_subjects(self):
        subjects = Subject.get_by_teacher(self.teacher_id)
        if subjects:
            self.display.table_header(["ID", "Code", "Name", "Description", "Course"])
            for s in subjects:
                self.display.table_row([s[0], s[1], s[2], s[3] or "N/A", s[4] or "N/A"])
        else:
            self.display.info("No subjects found")
        input("\nPress Enter to continue...")

    def add_subject(self):
        self.view_courses()
        code = input("Subject Code: ")
        name = input("Subject Name: ")
        description = input("Description: ")
        course_id = input("Course ID: ")
        
        result = Subject.create(code, name, description, self.teacher_id, course_id)
        if result:
            self.display.success("Subject added successfully!")
        else:
            self.display.error("Failed to add subject")
        input("\nPress Enter to continue...")

    def update_subject(self):
        self.view_subjects()
        subject_id = input("Enter Subject ID to update: ")
        code = input("New Code: ")
        name = input("New Name: ")
        description = input("New Description: ")
        course_id = input("New Course ID: ")
        
        result = Subject.update(subject_id, code, name, description, course_id)
        if result:
            self.display.success("Subject updated successfully!")
        else:
            self.display.error("Failed to update subject")
        input("\nPress Enter to continue...")

    def delete_subject(self):
        self.view_subjects()
        subject_id = input("Enter Subject ID to delete: ")
        
        result = Subject.delete(subject_id)
        if result:
            self.display.success("Subject deleted successfully!")
        else:
            self.display.error("Failed to delete subject")
        input("\nPress Enter to continue...")

    def view_courses(self):
        courses = Course.get_all()
        if courses:
            self.display.table_header(["ID", "Name", "Description"])
            for c in courses:
                self.display.table_row([c[0], c[1], c[2] or "N/A"])

    def manage_enrollments(self):
        while True:
            self.display.header("ENROLLMENT MANAGEMENT")
            self.display.menu([
                "View Pending Enrollments",
                "Approve/Deny Enrollments"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_pending_enrollments()
            elif choice == '2':
                self.approve_deny_enrollments()
            elif choice == '0':
                break

    def view_pending_enrollments(self):
        enrollments = Enrollment.get_pending_by_teacher(self.teacher_id)
        if enrollments:
            self.display.table_header(["ID", "Student", "Subject Code", "Subject Name", "Date"])
            for e in enrollments:
                self.display.table_row([e[0], e[1], e[2], e[3], str(e[4])[:10]])
        else:
            self.display.info("No pending enrollments")
        input("\nPress Enter to continue...")

    def approve_deny_enrollments(self):
        self.view_pending_enrollments()
        enrollment_id = input("Enter Enrollment ID: ")
        status = input("Enter status (approved/denied): ").lower()
        
        if status in ['approved', 'denied']:
            result = Enrollment.update_status(enrollment_id, status)
            if result:
                self.display.success(f"Enrollment {status} successfully!")
            else:
                self.display.error("Failed to update enrollment")
        else:
            self.display.error("Invalid status")
        input("\nPress Enter to continue...")

    def manage_grades(self):
        while True:
            self.display.header("GRADE MANAGEMENT")
            self.display.menu([
                "View Students",
                "Enter/Update Grades"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_enrolled_students()
            elif choice == '2':
                self.enter_grades()
            elif choice == '0':
                break

    def view_enrolled_students(self):
        students = Enrollment.get_approved_by_teacher(self.teacher_id)
        if students:
            self.display.table_header(["Enrollment ID", "Student", "Subject Code", "Subject Name"])
            for s in students:
                self.display.table_row([s[0], s[1], s[2], s[3]])
        else:
            self.display.info("No enrolled students")
        input("\nPress Enter to continue...")

    def enter_grades(self):
        self.view_enrolled_students()
        enrollment_id = input("Enter Enrollment ID: ")
        grade = input("Enter Grade (0-100): ")
        remarks = input("Enter Remarks: ")
        
        try:
            grade_val = float(grade)
            if 0 <= grade_val <= 100:
                result = Grade.create_or_update(enrollment_id, grade_val, remarks)
                if result:
                    self.display.success("Grade saved successfully!")
                else:
                    self.display.error("Failed to save grade")
            else:
                self.display.error("Grade must be between 0-100")
        except ValueError:
            self.display.error("Invalid grade format")
        input("\nPress Enter to continue...")