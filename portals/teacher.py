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
                "Manage Grades",
                "View Grade Statistics"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.manage_subjects()
            elif choice == '2':
                self.manage_enrollments()
            elif choice == '3':
                self.manage_grades()
            elif choice == '4':
                self.view_grade_statistics()
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
        if result is not None:
            self.display.success("Subject updated successfully!")
        else:
            self.display.error("Failed to update subject")
        input("\nPress Enter to continue...")

    def delete_subject(self):
        self.view_subjects()
        subject_id = input("Enter Subject ID to delete: ")
        
        result = Subject.delete(subject_id)
        if result is not None:
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
            if result is not None:
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
                "View Students with Grades",
                "Enter/Update Component Grades",
                "Enter/Update Simple Grade (Legacy)",
                "View Detailed Grade Report"
            ])
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                self.view_enrolled_students()
            elif choice == '2':
                self.enter_component_grades()
            elif choice == '3':
                self.enter_simple_grades()
            elif choice == '4':
                self.view_detailed_grades()
            elif choice == '0':
                break

    def view_enrolled_students(self):
        students = Enrollment.get_approved_by_teacher(self.teacher_id)
        if students:
            self.display.table_header(["Enrollment ID", "Student", "Subject Code", "Subject Name", "Final Grade", "Type"])
            for s in students:
                grade_data = Grade.get_detailed_by_enrollment(s[0])
                if grade_data:
                    if grade_data['is_component_based']:
                        grade_display = f"{grade_data['final_grade']:.2f}" if grade_data['final_grade'] is not None else "N/A"
                        grade_type = "Component"
                    else:
                        grade_display = f"{grade_data['legacy_grade']:.2f}" if grade_data['legacy_grade'] is not None else "N/A"
                        grade_type = "Legacy"
                else:
                    grade_display = "N/A"
                    grade_type = "None"
                
                self.display.table_row([s[0], s[1], s[2], s[3], grade_display, grade_type])
        else:
            self.display.info("No enrolled students")
        input("\nPress Enter to continue...")

    def enter_component_grades(self):
        self.view_enrolled_students()
        enrollment_id = input("Enter Enrollment ID: ")
        
        print("\n=== COMPONENT GRADING SYSTEM ===")
        print("Default weights: Activity (40%), Quiz (20%), Exam (40%)")
        print("You can customize these weights or use defaults.")
        
        # Get current grade data if exists
        current_grade = Grade.get_detailed_by_enrollment(enrollment_id)
        
        # Activity Score
        activity_default = current_grade['activity_score'] if current_grade and current_grade['activity_score'] is not None else ""
        activity_score = input(f"Activity Score (0-100) [{activity_default}]: ").strip()
        if not activity_score and activity_default:
            activity_score = str(activity_default)
        
        # Quiz Score
        quiz_default = current_grade['quiz_score'] if current_grade and current_grade['quiz_score'] is not None else ""
        quiz_score = input(f"Quiz Score (0-100) [{quiz_default}]: ").strip()
        if not quiz_score and quiz_default:
            quiz_score = str(quiz_default)
        
        # Exam Score
        exam_default = current_grade['exam_score'] if current_grade and current_grade['exam_score'] is not None else ""
        exam_score = input(f"Exam Score (0-100) [{exam_default}]: ").strip()
        if not exam_score and exam_default:
            exam_score = str(exam_default)
        
        # Weights (optional customization)
        print("\n--- Weight Configuration (Optional) ---")
        activity_weight_default = current_grade['activity_weight'] if current_grade and current_grade['activity_weight'] is not None else 40.0
        quiz_weight_default = current_grade['quiz_weight'] if current_grade and current_grade['quiz_weight'] is not None else 20.0
        exam_weight_default = current_grade['exam_weight'] if current_grade and current_grade['exam_weight'] is not None else 40.0
        
        activity_weight = input(f"Activity Weight (%) [{activity_weight_default}]: ").strip()
        if not activity_weight:
            activity_weight = str(activity_weight_default)
        
        quiz_weight = input(f"Quiz Weight (%) [{quiz_weight_default}]: ").strip()
        if not quiz_weight:
            quiz_weight = str(quiz_weight_default)
        
        exam_weight = input(f"Exam Weight (%) [{exam_weight_default}]: ").strip()
        if not exam_weight:
            exam_weight = str(exam_weight_default)
        
        try:
            activity_val = float(activity_score)
            quiz_val = float(quiz_score)
            exam_val = float(exam_score)
            activity_weight_val = float(activity_weight)
            quiz_weight_val = float(quiz_weight)
            exam_weight_val = float(exam_weight)
            
            # Validate scores
            if not (0 <= activity_val <= 100 and 0 <= quiz_val <= 100 and 0 <= exam_val <= 100):
                self.display.error("All scores must be between 0-100")
                input("\nPress Enter to continue...")
                return
            
            # Calculate and preview final grade
            final_grade = Grade.calculate_final_grade(activity_val, quiz_val, exam_val, 
                                                    activity_weight_val, quiz_weight_val, exam_weight_val)
            remarks = "Passed" if final_grade >= 75 else "Failed"
            
            print(f"\n=== GRADE PREVIEW ===")
            print(f"Activity: {activity_val:.2f} ({activity_weight_val}%)")
            print(f"Quiz: {quiz_val:.2f} ({quiz_weight_val}%)")
            print(f"Exam: {exam_val:.2f} ({exam_weight_val}%)")
            print(f"Final Grade: {final_grade:.2f}")
            print(f"Remarks: {remarks}")
            
            confirm = input("\nSave this grade? (y/n): ").lower()
            if confirm == 'y':
                result = Grade.create_or_update(
                    enrollment_id=enrollment_id,
                    activity_score=activity_val,
                    quiz_score=quiz_val,
                    exam_score=exam_val,
                    activity_weight=activity_weight_val,
                    quiz_weight=quiz_weight_val,
                    exam_weight=exam_weight_val,
                    is_component_based=True
                )
                
                if result is not None:
                    self.display.success("Component grades saved successfully!")
                else:
                    self.display.error("Failed to save grades")
            else:
                self.display.info("Grade entry cancelled")
                
        except ValueError:
            self.display.error("Invalid number format")
        
        input("\nPress Enter to continue...")

    def enter_simple_grades(self):
        self.view_enrolled_students()
        enrollment_id = input("Enter Enrollment ID: ")
        grade = input("Enter Grade (0-100): ")
        remarks = input("Enter Remarks: ")
        
        try:
            grade_val = float(grade)
            if 0 <= grade_val <= 100:
                result = Grade.create_or_update(enrollment_id, grade_val, remarks, is_component_based=False)
                if result is not None:
                    self.display.success("Grade saved successfully!")
                else:
                    self.display.error("Failed to save grade")
            else:
                self.display.error("Grade must be between 0-100")
        except ValueError:
            self.display.error("Invalid grade format")
        input("\nPress Enter to continue...")

    def view_detailed_grades(self):
        students = Enrollment.get_approved_by_teacher(self.teacher_id)
        if not students:
            self.display.info("No enrolled students")
            input("\nPress Enter to continue...")
            return
        
        print("\n" + "="*80)
        print("DETAILED GRADE REPORT".center(80))
        print("="*80)
        
        for s in students:
            grade_data = Grade.get_detailed_by_enrollment(s[0])
            print(f"\nStudent: {s[1]} | Subject: {s[2]} - {s[3]}")
            print("-" * 60)
            
            if grade_data and grade_data['is_component_based']:
                print("Grade Type: Component-Based")
                print(f"Activity Score: {grade_data['activity_score']:.2f} (Weight: {grade_data['activity_weight']:.1f}%)")
                print(f"Quiz Score: {grade_data['quiz_score']:.2f} (Weight: {grade_data['quiz_weight']:.1f}%)")
                print(f"Exam Score: {grade_data['exam_score']:.2f} (Weight: {grade_data['exam_weight']:.1f}%)")
                print(f"Final Grade: {grade_data['final_grade']:.2f}")
                print(f"Remarks: {grade_data['remarks']}")
            elif grade_data and not grade_data['is_component_based']:
                print("Grade Type: Legacy")
                print(f"Grade: {grade_data['legacy_grade']:.2f}")
                print(f"Remarks: {grade_data['remarks']}")
            else:
                print("Grade Type: Not Set")
                print("No grade recorded yet")
        
        input("\nPress Enter to continue...")

    def view_grade_statistics(self):
        stats = Grade.get_grade_statistics()
        if stats:
            self.display.header("GRADE STATISTICS")
            print(f"Total Grades: {stats[0]}")
            print(f"Average Grade: {stats[1]:.2f}" if stats[1] else "Average Grade: N/A")
            print(f"Passed Students: {stats[2] or 0}")
            print(f"Failed Students: {stats[3] or 0}")
            
            if stats[0] > 0:
                pass_rate = (stats[2] / stats[0]) * 100 if stats[2] else 0
                print(f"Pass Rate: {pass_rate:.1f}%")
        else:
            self.display.info("No grade statistics available")
        
        input("\nPress Enter to continue...")