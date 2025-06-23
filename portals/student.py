from utils import Display
from models.user import Student
from models.enrollment import Enrollment
from models.grade import Grade
from models.subject import Subject

class StudentPortal:
    def __init__(self, user):
        self.user = user
        self.display = Display()
        student_data = Student.get_by_user_id(user['user_id'])
        if student_data:
            self.student_id = student_data[0]
            self.student_name = student_data[1]
            self.course = student_data[2]
            self.year_level = student_data[3]
        else:
            self.student_id = None

    def show_menu(self):
        if not self.student_id:
            self.display.error("Student data not found")
            return
            
        while True:
            self.display.header("STUDENT PORTAL")
            self.display_student_info()
            self.display.menu([
                "View Enrolled Subjects",
                "View Grades",
                "Enroll in Subject"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_enrolled_subjects()
            elif choice == '2':
                self.view_grades()
            elif choice == '3':
                self.enroll_subject()
            elif choice == '0':
                break

    def display_student_info(self):
        self.display.info(f"Student Name: {self.student_name}")
        course_display = self.course if self.course else "N/A"
        self.display.info(f"Course: {course_display}")
        self.display.info(f"Year Level: {self.year_level}")
        print()

    def view_enrolled_subjects(self):
        enrollments = Enrollment.get_by_student(self.student_id)
        if enrollments:
            self.display.table_header(["Subject Code", "Subject Name", "Status"])
            for e in enrollments:
                self.display.table_row([e[1], e[2], e[3]])
        else:
            self.display.info("No enrolled subjects")
        input("\nPress Enter to continue...")

    def view_grades(self):
        grades = Grade.get_by_student(self.student_id)
        if grades:
            self.display.table_header(["Subject Code", "Subject Name", "Grade", "Remarks"])
            for g in grades:
                self.display.table_row([g[0], g[1], f"{g[2]:.2f}" if g[2] else "N/A", g[3] or "N/A"])
        else:
            self.display.info("No grades available")
        input("\nPress Enter to continue...")

    def enroll_subject(self):
        subjects = Subject.get_all()
        if subjects:
            self.display.table_header(["ID", "Code", "Name", "Description", "Teacher", "Course"])
            for s in subjects:
                self.display.table_row([s[0], s[1], s[2], s[3] or "N/A", s[4] or "N/A", s[5] or "N/A"])
            
            subject_id = input("\nEnter Subject ID to enroll: ")
            result = Enrollment.create(self.student_id, subject_id)
            if result:
                self.display.success("Enrollment request submitted!")
            else:
                self.display.error("Failed to submit enrollment (may already be enrolled)")
        else:
            self.display.info("No subjects available")
        input("\nPress Enter to continue...")