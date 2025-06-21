# ==============================================================================
# MODELS (models/course.py)
# ==============================================================================

from dataclasses import dataclass
from typing import Optional, List
from database.db import db

@dataclass
class Course:
    course_id: int
    course_code: str
    course_name: str
    description: Optional[str] = None
    credits: int = 3
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def get_all_active() -> List['Course']:
        """Get all active courses"""
        results = db.execute_query("""
            SELECT course_id, course_code, course_name, description, credits, 
                   is_active, created_at, updated_at
            FROM courses 
            WHERE is_active = TRUE
            ORDER BY course_code
        """)

        return [Course(
            course_id=row[0], course_code=row[1], course_name=row[2],
            description=row[3], credits=row[4], is_active=row[5],
            created_at=row[6], updated_at=row[7]
        ) for row in results]

    @staticmethod
    def find_by_id(course_id: int) -> Optional['Course']:
        """Find course by ID"""
        result = db.execute_query("""
            SELECT course_id, course_code, course_name, description, credits, 
                   is_active, created_at, updated_at
            FROM courses WHERE course_id = %s
        """, (course_id,))

        if result:
            row = result[0]
            return Course(
                course_id=row[0], course_code=row[1], course_name=row[2],
                description=row[3], credits=row[4], is_active=row[5],
                created_at=row[6], updated_at=row[7]
            )
        return None
