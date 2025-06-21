# ==============================================================================
# MODELS (models/student.py)
# ==============================================================================

import random
import string
from datetime import date
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Student:
    student_id: str
    full_name: str
    course_id: int
    year_level: int
    email: Optional[str] = None
    status: str = 'active'
    enrollment_date: Optional[date] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Related data (populated via joins)
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    
    @staticmethod
    def generate_id() -> str:
        """Generate unique 8-digit student ID"""
        while True:
            sid = ''.join(random.choices(string.digits, k=8))
            if not Student.exists(sid):
                return sid
    
    @staticmethod
    def exists(student_id: str) -> bool:
        """Check if student ID exists"""
        result = db.execute_query(
            "SELECT 1 FROM students WHERE student_id = %s", (student_id,))
        return len(result) > 0
    
    def save(self) -> bool:
        """Save student to database"""
        try:
            if self.exists(self.student_id):
                # Update existing student
                db.execute_update("""
                    UPDATE students 
                    SET full_name=%s, email=%s, course_id=%s, year_level=%s, status=%s
                    WHERE student_id=%s
                """, (self.full_name, self.email, self.course_id, 
                      self.year_level, self.status, self.student_id))
            else:
                # Insert new student
                db.execute_update("""
                    INSERT INTO students (student_id, full_name, email, course_id, year_level, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.student_id, self.full_name, self.email, 
                      self.course_id, self.year_level, self.status))
                
                # Create initial grade record
                db.execute_update(
                    "INSERT INTO grades (student_id) VALUES (%s)", (self.student_id,))
            return True
        except DatabaseError:
            return False
    
    @staticmethod
    def find_by_id(student_id: str) -> Optional['Student']:
        """Find student by ID with course information"""
        result = db.execute_query("""
            SELECT s.student_id, s.full_name, s.email, s.course_id, s.year_level, 
                   s.status, s.enrollment_date, s.created_at, s.updated_at,
                   c.course_code, c.course_name
            FROM students s
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.student_id = %s
        """, (student_id,))
        
        if result:
            row = result[0]
            return Student(
                student_id=row[0], full_name=row[1], email=row[2],
                course_id=row[3], year_level=row[4], status=row[5],
                enrollment_date=row[6], created_at=row[7], updated_at=row[8],
                course_code=row[9], course_name=row[10]
            )
        return None
    
    @staticmethod
    def find_by_course(course_id: int) -> List['Student']:
        """Find all students in a course"""
        results = db.execute_query("""
            SELECT s.student_id, s.full_name, s.email, s.course_id, s.year_level, 
                   s.status, s.enrollment_date, s.created_at, s.updated_at,
                   c.course_code, c.course_name
            FROM students s
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.course_id = %s AND s.status = 'active'
            ORDER BY s.full_name
        """, (course_id,))
        
        return [Student(
            student_id=row[0], full_name=row[1], email=row[2],
            course_id=row[3], year_level=row[4], status=row[5],
            enrollment_date=row[6], created_at=row[7], updated_at=row[8],
            course_code=row[9], course_name=row[10]
        ) for row in results]
    
    @staticmethod
    def get_all() -> List['Student']:
        """Get all active students with course information"""
        results = db.execute_query("""
            SELECT s.student_id, s.full_name, s.email, s.course_id, s.year_level, 
                   s.status, s.enrollment_date, s.created_at, s.updated_at,
                   c.course_code, c.course_name
            FROM students s
            JOIN courses c ON s.course_id = c.course_id
            WHERE s.status = 'active'
            ORDER BY s.full_name
        """)
        
        return [Student(
            student_id=row[0], full_name=row[1], email=row[2],
            course_id=row[3], year_level=row[4], status=row[5],
            enrollment_date=row[6], created_at=row[7], updated_at=row[8],
            course_code=row[9], course_name=row[10]
        ) for row in results]