# ==============================================================================
# SERVICES (services/grading_service.py)
# ==============================================================================
from typing import List, Optional, Tuple
from models.grade import Grade
from models.student import Student
from database.db import db



class GradingService:
    @staticmethod
    def update_grades(student_id: str, quiz: float, activity: float, exam: float, 
                    changed_by: str = 'system') -> Tuple[bool, str]:
        """Update student grades with validation"""
        try:
            # Validate student exists
            student = Student.find_by_id(student_id)
            if not student:
                return False, "Student not found"
            
            # Validate grade ranges
            if not all(0 <= grade <= 100 for grade in [quiz, activity, exam]):
                return False, "Grades must be between 0 and 100"
            
            # Get or create grade record
            grade = Grade.find_by_student_id(student_id)
            if not grade:
                grade = Grade(student_id=student_id)
            
            grade.quiz = quiz
            grade.activity = activity
            grade.exam = exam
            
            if grade.save(changed_by):
                return True, "Grades updated successfully"
            else:
                return False, "Failed to update grades"
                
        except Exception as e:
            return False, f"Grading error: {str(e)}"
    
    @staticmethod
    def calculate_final_scores() -> None:
        """Recalculate all final scores (triggered after settings change)"""
        # MySQL will automatically recalculate due to generated column
        pass
    
    @staticmethod
    def get_grade_report(course_id: Optional[int] = None) -> List[Grade]:
        """Get grade report for all students or specific course"""
        if course_id:
            results = db.execute_query("""
                SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                       g.letter_grade, g.created_at, g.updated_at,
                       s.full_name, c.course_code
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                JOIN courses c ON s.course_id = c.course_id
                WHERE s.course_id = %s AND s.status = 'active'
                ORDER BY g.final_score DESC
            """, (course_id,))
        else:
            results = db.execute_query("""
                SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                       g.letter_grade, g.created_at, g.updated_at,
                       s.full_name, c.course_code
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                JOIN courses c ON s.course_id = c.course_id
                WHERE s.status = 'active'
                ORDER BY g.final_score DESC
            """)
        
        return [Grade(
            student_id=row[0], quiz=row[1], activity=row[2], exam=row[3],
            final_score=row[4], letter_grade=row[5], created_at=row[6],
            updated_at=row[7], student_name=row[8], course_code=row[9]
        ) for row in results]
    
    @staticmethod
    def get_top_performers(limit: int = 10) -> List[Grade]:
        """Get top performing students"""
        results = db.execute_query("""
            SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                   g.letter_grade, g.created_at, g.updated_at,
                   s.full_name, c.course_code
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.status = 'active' AND g.final_score IS NOT NULL
            ORDER BY g.final_score DESC
            LIMIT %s
        """, (limit,))
        
        return [Grade(
            student_id=row[0], quiz=row[1], activity=row[2], exam=row[3],
            final_score=row[4], letter_grade=row[5], created_at=row[6],
            updated_at=row[7], student_name=row[8], course_code=row[9]
        ) for row in results]
    
    @staticmethod
    def get_at_risk_students(threshold: float = 60.0) -> List[Grade]:
        """Get students below passing threshold"""
        results = db.execute_query("""
            SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                   g.letter_grade, g.created_at, g.updated_at,
                   s.full_name, c.course_code
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.status = 'active' AND g.final_score < %s
            ORDER BY g.final_score ASC
        """, (threshold,))
        
        return [Grade(
            student_id=row[0], quiz=row[1], activity=row[2], exam=row[3],
            final_score=row[4], letter_grade=row[5], created_at=row[6],
            updated_at=row[7], student_name=row[8], course_code=row[9]
        ) for row in results]