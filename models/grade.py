# ==============================================================================
# MODELS (models/grade.py)
# ==============================================================================
from dataclasses import dataclass
from typing import Optional, List
from database.db import db


@dataclass
class Grade:
    student_id: str
    quiz: float = 0.0
    activity: float = 0.0
    exam: float = 0.0
    final_score: Optional[float] = None
    letter_grade: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Student info (from joins)
    student_name: Optional[str] = None
    course_code: Optional[str] = None
    
    def calculate_letter_grade(self) -> str:
        """Calculate letter grade based on final score"""
        if self.final_score is None:
            return 'N/A'
        
        score = self.final_score
        if score >= 97: return 'A+'
        elif score >= 93: return 'A'
        elif score >= 90: return 'A-'
        elif score >= 87: return 'B+'
        elif score >= 83: return 'B'
        elif score >= 80: return 'B-'
        elif score >= 77: return 'C+'
        elif score >= 73: return 'C'
        elif score >= 70: return 'C-'
        elif score >= 67: return 'D+'
        elif score >= 65: return 'D'
        else: return 'F'
    
    def save(self, changed_by: str = 'system') -> bool:
        """Save grade with audit trail"""
        try:
            # Get current grades for audit
            current = Grade.find_by_student_id(self.student_id)
            
            # Update grades
            db.execute_update("""
                UPDATE grades 
                SET quiz=%s, activity=%s, exam=%s, letter_grade=%s
                WHERE student_id=%s
            """, (self.quiz, self.activity, self.exam, 
                  self.calculate_letter_grade(), self.student_id))
            
            # Log changes in audit table
            if current:
                changes = []
                if current.quiz != self.quiz:
                    changes.append(('quiz', current.quiz, self.quiz))
                if current.activity != self.activity:
                    changes.append(('activity', current.activity, self.activity))
                if current.exam != self.exam:
                    changes.append(('exam', current.exam, self.exam))
                
                for grade_type, old_val, new_val in changes:
                    db.execute_update("""
                        INSERT INTO grade_audit (student_id, grade_type, old_value, new_value, changed_by)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (self.student_id, grade_type, old_val, new_val, changed_by))
            
            return True
        except DatabaseError:
            return False
    
    @staticmethod
    def find_by_student_id(student_id: str) -> Optional['Grade']:
        """Find grade by student ID"""
        result = db.execute_query("""
            SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                   g.letter_grade, g.created_at, g.updated_at,
                   s.full_name, c.course_code
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            JOIN courses c ON s.course_id = c.course_id
            WHERE g.student_id = %s
        """, (student_id,))
        
        if result:
            row = result[0]
            return Grade(
                student_id=row[0], quiz=row[1], activity=row[2], exam=row[3],
                final_score=row[4], letter_grade=row[5], created_at=row[6],
                updated_at=row[7], student_name=row[8], course_code=row[9]
            )
        return None
    
    @staticmethod
    def get_all_with_student_info() -> List['Grade']:
        """Get all grades with student information"""
        results = db.execute_query("""
            SELECT g.student_id, g.quiz, g.activity, g.exam, g.final_score, 
                   g.letter_grade, g.created_at, g.updated_at,
                   s.full_name, c.course_code
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.status = 'active'
            ORDER BY s.full_name
        """)
        
        return [Grade(
            student_id=row[0], quiz=row[1], activity=row[2], exam=row[3],
            final_score=row[4], letter_grade=row[5], created_at=row[6],
            updated_at=row[7], student_name=row[8], course_code=row[9]
        ) for row in results]

@dataclass
class GradeSettings:
    quiz_weight: float = 0.30
    activity_weight: float = 0.30
    exam_weight: float = 0.40
    passing_grade: float = 60.0
    
    @staticmethod
    def get_current() -> 'GradeSettings':
        """Get current grade settings"""
        result = db.execute_query("""
            SELECT quiz_weight, activity_weight, exam_weight, passing_grade
            FROM grade_settings WHERE id = 1
        """)
        
        if result:
            row = result[0]
            return GradeSettings(
                quiz_weight=row[0], activity_weight=row[1],
                exam_weight=row[2], passing_grade=row[3]
            )
        return GradeSettings()  # Default values
    
    def save(self) -> bool:
        """Save grade settings"""
        try:
            db.execute_update("""
                UPDATE grade_settings 
                SET quiz_weight=%s, activity_weight=%s, exam_weight=%s, passing_grade=%s
                WHERE id=1
            """, (self.quiz_weight, self.activity_weight, self.exam_weight, self.passing_grade))
            return True
        except DatabaseError:
            return False
