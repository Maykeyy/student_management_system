import sys
from typing import Optional

# ==== Required Imports ====
from services.student_service import StudentService
from services.grading_service import GradingService
from services.reporting_service import ReportingService

from models.course import Course
from models.grade import Grade, GradeSettings
from utils.validators import InputHelper

from utils.display import DisplayHelper
from utils.validators import InputValidator

from database.db import db


class StudentManagementCLI:
    def __init__(self):
        self.student_service = StudentService()
        self.grading_service = GradingService()
        self.reporting_service = ReportingService()
        
        # Initialize database schema
        try:
            db.setup_schema()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Database initialization error: {e}")
            sys.exit(1)
    
    def run(self):
        """Main application loop"""
        DisplayHelper.print_header("STUDENT MANAGEMENT SYSTEM", 80)
        print("Welcome to the Student Management System!")
        
        while True:
            try:
                self.show_main_menu()
                choice = input("\nSelect an option: ").strip()
                
                if choice == '1':
                    self.register_student_menu()
                elif choice == '2':
                    self.view_students_menu()
                elif choice == '3':
                    self.edit_grades_menu()
                elif choice == '4':
                    self.reports_menu()
                elif choice == '5':
                    self.settings_menu()
                elif choice == '6':
                    if InputHelper.confirm_action("Are you sure you want to exit?"):
                        print("Thank you for using Student Management System. Goodbye!")
                        break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again or contact support.")
    
    def show_main_menu(self):
        """Display main menu options"""
        DisplayHelper.print_header("MAIN MENU", 60, "-")
        options = [
            "1. Register Student",
            "2. View Students",
            "3. Edit Student Grades",
            "4. Reports & Analytics",
            "5. System Settings",
            "6. Exit"
        ]
        for option in options:
            print(f"   {option}")
    
    def register_student_menu(self):
        """Handle student registration"""
        DisplayHelper.print_header("STUDENT REGISTRATION")
        
        try:
            # Get student details
            print("Enter student information:")
            
            full_name = InputHelper.get_validated_input(
                "Full Name: ",
                InputValidator.validate_name,
                "Please enter a valid name (2-255 characters, letters only)"
            )
            
            email = InputHelper.get_validated_input(
                "Email (optional): ",
                InputValidator.validate_email,
                "Please enter a valid email address"
            )
            
            # Show available courses
            courses = Course.get_all_active()
            if not courses:
                print("No active courses available. Please contact administrator.")
                return
            
            print("\nAvailable Courses:")
            headers = ["ID", "Code", "Course Name", "Credits"]
            rows = [[c.course_id, c.course_code, c.course_name, c.credits] for c in courses]
            DisplayHelper.print_table(headers, rows)
            
            valid_course_ids = [str(c.course_id) for c in courses]
            course_choice = InputHelper.get_choice(
                "Select Course ID: ",
                valid_course_ids
            )
            
            year_level = InputHelper.get_validated_input(
                "Year Level (1-4): ",
                InputValidator.validate_year_level,
                "Year level must be 1, 2, 3, or 4"
            )
            
            # Confirm registration
            print("\nRegistration Summary:")
            print(f"Name: {full_name}")
            print(f"Email: {email or 'Not provided'}")
            print(f"Course: {next(c.course_name for c in courses if c.course_id == int(course_choice))}")
            print(f"Year Level: {year_level}")
            
            if InputHelper.confirm_action("Proceed with registration?"):
                success, message = self.student_service.register_student(
                    full_name, email, int(course_choice), year_level
                )
                print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
            else:
                print("Registration cancelled.")
                
        except Exception as e:
            print(f"Registration error: {e}")
    
    def view_students_menu(self):
        """Handle student viewing options"""
        DisplayHelper.print_header("VIEW STUDENTS")
        
        options = [
            "1. View all students",
            "2. View students by course",
            "3. Search student by ID",
            "4. Back to main menu"
        ]
        
        for option in options:
            print(f"   {option}")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            students = self.student_service.get_all_students()
            DisplayHelper.print_student_list(students, show_grades=True)
            
        elif choice == '2':
            courses = Course.get_all_active()
            if not courses:
                print("No courses available.")
                return
            
            print("\nAvailable Courses:")
            headers = ["ID", "Code", "Course Name"]
            rows = [[c.course_id, c.course_code, c.course_name] for c in courses]
            DisplayHelper.print_table(headers, rows)
            
            valid_course_ids = [str(c.course_id) for c in courses]
            course_choice = InputHelper.get_choice("Select Course ID: ", valid_course_ids)
            
            students = self.student_service.get_students_by_course(int(course_choice))
            course_name = next(c.course_name for c in courses if c.course_id == int(course_choice))
            
            DisplayHelper.print_subheader(f"Students in {course_name}")
            DisplayHelper.print_student_list(students, show_grades=True)
            
        elif choice == '3':
            student_id = InputHelper.get_validated_input(
                "Enter Student ID: ",
                InputValidator.validate_student_id,
                "Student ID must be exactly 8 digits"
            )
            
            student = self.student_service.find_student(student_id)
            if student:
                print(f"\nStudent Found:")
                DisplayHelper.print_student_list([student], show_grades=True)
            else:
                print("Student not found.")
        
        elif choice == '4':
            return
        else:
            print("Invalid choice.")
    
    def edit_grades_menu(self):
        """Handle grade editing"""
        DisplayHelper.print_header("EDIT STUDENT GRADES")
        
        student_id = InputHelper.get_validated_input(
            "Enter Student ID: ",
            InputValidator.validate_student_id,
            "Student ID must be exactly 8 digits"
        )
        
        # Verify student exists
        student = self.student_service.find_student(student_id)
        if not student:
            print("Student not found.")
            return
        
        # Show current grades
        current_grade = Grade.find_by_student_id(student_id)
        print(f"\nEditing grades for: {student.full_name} (ID: {student_id})")
        print(f"Course: {student.course_name}")
        
        if current_grade:
            print(f"\nCurrent Grades:")
            print(f"Quiz: {current_grade.quiz}")
            print(f"Activity: {current_grade.activity}")
            print(f"Exam: {current_grade.exam}")
            print(f"Final Score: {current_grade.final_score or 'Not calculated'}")
            print(f"Letter Grade: {current_grade.letter_grade or 'Not assigned'}")
        
        # Get new grades
        print(f"\nEnter new grades (0-100):")
        
        quiz = InputHelper.get_validated_input(
            "Quiz Grade: ",
            InputValidator.validate_grade,
            "Grade must be between 0 and 100"
        )
        
        activity = InputHelper.get_validated_input(
            "Activity Grade: ",
            InputValidator.validate_grade,
            "Grade must be between 0 and 100"
        )
        
        exam = InputHelper.get_validated_input(
            "Exam Grade: ",
            InputValidator.validate_grade,
            "Grade must be between 0 and 100"
        )
        
        # Show preview
        settings = GradeSettings.get_current()
        final_score = (quiz * settings.quiz_weight + 
                      activity * settings.activity_weight + 
                      exam * settings.exam_weight)
        
        print(f"\nGrade Preview:")
        print(f"Quiz: {quiz} (Weight: {settings.quiz_weight:.1%})")
        print(f"Activity: {activity} (Weight: {settings.activity_weight:.1%})")
        print(f"Exam: {exam} (Weight: {settings.exam_weight:.1%})")
        print(f"Calculated Final Score: {final_score:.2f}")
        
        if InputHelper.confirm_action("Save these grades?"):
            success, message = self.grading_service.update_grades(
                student_id, quiz, activity, exam, "CLI User"
            )
            print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
        else:
            print("Grade update cancelled.")
    
    def reports_menu(self):
        """Handle reports and analytics"""
        DisplayHelper.print_header("REPORTS & ANALYTICS")
        
        options = [
            "1. Overall Statistics",
            "2. Course Statistics",
            "3. Top Performers",
            "4. At-Risk Students",
            "5. Grade Distribution Report",
            "6. Back to main menu"
        ]
        
        for option in options:
            print(f"   {option}")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            stats = self.reporting_service.get_overall_statistics()
            DisplayHelper.print_statistics(stats, "Overall System Statistics")
            
        elif choice == '2':
            courses = Course.get_all_active()
            if not courses:
                print("No courses available.")
                return
            
            print("\nAvailable Courses:")
            headers = ["ID", "Code", "Course Name"]
            rows = [[c.course_id, c.course_code, c.course_name] for c in courses]
            DisplayHelper.print_table(headers, rows)
            
            valid_course_ids = [str(c.course_id) for c in courses]
            course_choice = InputHelper.get_choice("Select Course ID: ", valid_course_ids)
            
            stats = self.reporting_service.get_course_statistics(int(course_choice))
            course_name = next(c.course_name for c in courses if c.course_id == int(course_choice))
            DisplayHelper.print_statistics(stats, f"Statistics for {course_name}")
            
        elif choice == '3':
            try:
                limit = int(input("Number of top performers to show (default 10): ") or "10")
                top_performers = self.grading_service.get_top_performers(limit)
                DisplayHelper.print_subheader(f"Top {limit} Performers")
                DisplayHelper.print_grade_report(top_performers)
            except ValueError:
                print("Invalid number entered.")
                
        elif choice == '4':
            settings = GradeSettings.get_current()
            at_risk = self.grading_service.get_at_risk_students(settings.passing_grade)
            DisplayHelper.print_subheader(f"Students Below {settings.passing_grade}%")
            DisplayHelper.print_grade_report(at_risk)
            
        elif choice == '5':
            print("\nSelect report scope:")
            print("1. All courses")
            print("2. Specific course")
            
            scope_choice = InputHelper.get_choice("Choice: ", ["1", "2"])
            
            if scope_choice == "1":
                grades = self.grading_service.get_grade_report()
                DisplayHelper.print_subheader("Complete Grade Report")
            else:
                courses = Course.get_all_active()
                if not courses:
                    print("No courses available.")
                    return
                
                print("\nAvailable Courses:")
                headers = ["ID", "Code", "Course Name"]
                rows = [[c.course_id, c.course_code, c.course_name] for c in courses]
                DisplayHelper.print_table(headers, rows)
                
                valid_course_ids = [str(c.course_id) for c in courses]
                course_choice = InputHelper.get_choice("Select Course ID: ", valid_course_ids)
                
                grades = self.grading_service.get_grade_report(int(course_choice))
                course_name = next(c.course_name for c in courses if c.course_id == int(course_choice))
                DisplayHelper.print_subheader(f"Grade Report for {course_name}")
            
            DisplayHelper.print_grade_report(grades)
            
        elif choice == '6':
            return
        else:
            print("Invalid choice.")
    
    def settings_menu(self):
        """Handle system settings"""
        DisplayHelper.print_header("SYSTEM SETTINGS")
        
        options = [
            "1. View Grade Weighting",
            "2. Update Grade Weighting",
            "3. Update Passing Grade Threshold",
            "4. Back to main menu"
        ]
        
        for option in options:
            print(f"   {option}")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            settings = GradeSettings.get_current()
            print(f"\nCurrent Grade Settings:")
            print(f"Quiz Weight: {settings.quiz_weight:.1%}")
            print(f"Activity Weight: {settings.activity_weight:.1%}")
            print(f"Exam Weight: {settings.exam_weight:.1%}")
            print(f"Passing Grade: {settings.passing_grade}%")
            
        elif choice == '2':
            settings = GradeSettings.get_current()
            print(f"\nCurrent weights:")
            print(f"Quiz: {settings.quiz_weight:.1%}")
            print(f"Activity: {settings.activity_weight:.1%}")
            print(f"Exam: {settings.exam_weight:.1%}")
            
            print(f"\nEnter new weights (must sum to 1.0):")
            
            quiz_weight = InputHelper.get_validated_input(
                "Quiz Weight (0.0-1.0): ",
                InputValidator.validate_weight,
                "Weight must be between 0.0 and 1.0"
            )
            
            activity_weight = InputHelper.get_validated_input(
                "Activity Weight (0.0-1.0): ",
                InputValidator.validate_weight,
                "Weight must be between 0.0 and 1.0"
            )
            
            exam_weight = InputHelper.get_validated_input(
                "Exam Weight (0.0-1.0): ",
                InputValidator.validate_weight,
                "Weight must be between 0.0 and 1.0"
            )
            
            total_weight = quiz_weight + activity_weight + exam_weight
            if abs(total_weight - 1.0) > 0.001:
                print(f"Error: Weights must sum to 1.0 (current sum: {total_weight:.3f})")
                return
            
            print(f"\nNew Weight Configuration:")
            print(f"Quiz: {quiz_weight:.1%}")
            print(f"Activity: {activity_weight:.1%}")
            print(f"Exam: {exam_weight:.1%}")
            
            if InputHelper.confirm_action("Apply these weights?"):
                new_settings = GradeSettings(
                    quiz_weight=quiz_weight,
                    activity_weight=activity_weight,
                    exam_weight=exam_weight,
                    passing_grade=settings.passing_grade
                )
                
                if new_settings.save():
                    print("Grade weights updated successfully!")
                    print("Note: Final scores will be automatically recalculated.")
                else:
                    print("Failed to update grade weights.")
            
        elif choice == '3':
            settings = GradeSettings.get_current()
            print(f"Current passing grade threshold: {settings.passing_grade}%")
            
            new_threshold = InputHelper.get_validated_input(
                "New passing grade threshold (0-100): ",
                InputValidator.validate_grade,
                "Threshold must be between 0 and 100"
            )
            
            if InputHelper.confirm_action(f"Set passing grade to {new_threshold}%?"):
                new_settings = GradeSettings(
                    quiz_weight=settings.quiz_weight,
                    activity_weight=settings.activity_weight,
                    exam_weight=settings.exam_weight,
                    passing_grade=new_threshold
                )
                
                if new_settings.save():
                    print("Passing grade threshold updated successfully!")
                else:
                    print("Failed to update passing grade threshold.")
                    
        elif choice == '4':
            return
        else:
            print("Invalid choice.")