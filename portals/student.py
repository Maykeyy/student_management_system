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
                "View Grades Summary",
                "View Detailed Grade Report",
                "Enroll in Subject"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_enrolled_subjects()
            elif choice == '2':
                self.view_grades_summary()
            elif choice == '3':
                self.view_detailed_grades()
            elif choice == '4':
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

    def view_grades_summary(self):
        grades = Grade.get_by_student(self.student_id)
        if grades:
            self.display.table_header(["Subject Code", "Subject Name", "Final Grade", "Remarks", "Type"])
            for g in grades:
                # g structure: code, name, legacy_grade, remarks, activity_score, quiz_score, exam_score, 
                # activity_weight, quiz_weight, exam_weight, final_grade, is_component_based
                if g[11]:  # is_component_based
                    final_grade = f"{g[10]:.2f}" if g[10] is not None else "N/A"
                    grade_type = "Component"
                else:
                    final_grade = f"{g[2]:.2f}" if g[2] is not None else "N/A"
                    grade_type = "Legacy"
                
                remarks = g[3] or "N/A"
                self.display.table_row([g[0], g[1], final_grade, remarks, grade_type])
        else:
            self.display.info("No grades available")
        input("\nPress Enter to continue...")

    def view_detailed_grades(self):
        grades = Grade.get_by_student(self.student_id)
        if not grades:
            self.display.info("No grades available")
            input("\nPress Enter to continue...")
            return
        
        print("\n" + "="*80)
        print("DETAILED GRADE REPORT".center(80))
        print("="*80)
        print(f"Student: {self.student_name}")
        print(f"Course: {self.course or 'N/A'} | Year Level: {self.year_level}")
        print("="*80)
        
        total_subjects = 0
        total_weighted_grade = 0
        passed_subjects = 0
        
        for g in grades:
            total_subjects += 1
            print(f"\nSubject: {g[0]} - {g[1]}")
            print("-" * 60)
            
            if g[11]:  # is_component_based
                print("Grading System: Component-Based")
                if g[4] is not None and g[5] is not None and g[6] is not None:
                    print(f"Activity Score: {g[4]:.2f} (Weight: {g[7]:.1f}%)")
                    print(f"Quiz Score: {g[5]:.2f} (Weight: {g[8]:.1f}%)")
                    print(f"Exam Score: {g[6]:.2f} (Weight: {g[9]:.1f}%)")
                    print(f"Final Grade: {g[10]:.2f}")
                    print(f"Remarks: {g[3] or 'N/A'}")
                    
                    # Add to GPA calculation
                    total_weighted_grade += g[10]
                    if g[10] >= 75:
                        passed_subjects += 1
                else:
                    print("Component scores not yet available")
            else:
                print("Grading System: Traditional")
                if g[2] is not None:
                    print(f"Grade: {g[2]:.2f}")
                    print(f"Remarks: {g[3] or 'N/A'}")
                    
                    # Add to GPA calculation
                    total_weighted_grade += g[2]
                    if g[2] >= 75:
                        passed_subjects += 1
                else:
                    print("Grade not yet available")
        
        # Display overall performance
        print("\n" + "="*80)
        print("OVERALL PERFORMANCE SUMMARY")
        print("="*80)
        print(f"Total Subjects: {total_subjects}")
        print(f"Subjects Passed: {passed_subjects}")
        print(f"Subjects Failed: {total_subjects - passed_subjects}")
        
        if total_subjects > 0:
            overall_average = total_weighted_grade / total_subjects
            pass_percentage = (passed_subjects / total_subjects) * 100
            print(f"Overall Average: {overall_average:.2f}")
            print(f"Pass Rate: {pass_percentage:.1f}%")
            
            # Performance indicator
            if overall_average >= 90:
                performance = "Excellent"
            elif overall_average >= 85:
                performance = "Very Good"
            elif overall_average >= 75:
                performance = "Good"
            else:
                performance = "Needs Improvement"
            print(f"Performance Level: {performance}")
        
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