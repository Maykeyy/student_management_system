# ==============================================================================
# SERVICES (services/student_service.py)
# ==============================================================================

from typing import List, Optional, Tuple
from models.student import Student



class StudentService:
    @staticmethod
    def register_student(full_name: str, email: str, course_id: int, year_level: int) -> Tuple[bool, str]:
        """Register a new student"""
        try:
            # Validate course exists
            course = Course.find_by_id(course_id)
            if not course:
                return False, "Invalid course selection"
            
            # Create student
            student = Student(
                student_id=Student.generate_id(),
                full_name=full_name.strip(),
                email=email.strip() if email else None,
                course_id=course_id,
                year_level=year_level
            )
            
            if student.save():
                return True, f"Student registered successfully with ID: {student.student_id}"
            else:
                return False, "Failed to register student"
                
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    @staticmethod
    def get_students_by_course(course_id: int) -> List[Student]:
        """Get all students in a specific course"""
        return Student.find_by_course(course_id)
    
    @staticmethod
    def get_all_students() -> List[Student]:
        """Get all active students"""
        return Student.get_all()
    
    @staticmethod
    def find_student(student_id: str) -> Optional[Student]:
        """Find student by ID"""
        return Student.find_by_id(student_id)
    
    @staticmethod
    def update_student_status(student_id: str, status: str) -> bool:
        """Update student status"""
        student = Student.find_by_id(student_id)
        if student:
            student.status = status
            return student.save()
        return False