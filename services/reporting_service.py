# ==============================================================================
# SERVICES (services/reporting_service.py)
# ==============================================================================
from typing import Dict, Any
from database.db import db


class ReportingService:
    @staticmethod
    def get_course_statistics(course_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics for a course"""
        result = db.execute_query("""
            SELECT 
                COUNT(*) as total_students,
                AVG(g.final_score) as avg_score,
                MIN(g.final_score) as min_score,
                MAX(g.final_score) as max_score,
                COUNT(CASE WHEN g.final_score >= 60 THEN 1 END) as passing_count,
                COUNT(CASE WHEN g.final_score < 60 THEN 1 END) as failing_count
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            WHERE s.course_id = %s AND s.status = 'active'
        """, (course_id,))
        
        if result and result[0][0] > 0:
            row = result[0]
            total = row[0]
            return {
                'total_students': total,
                'average_score': round(row[1] or 0, 2),
                'min_score': row[2] or 0,
                'max_score': row[3] or 0,
                'passing_count': row[4] or 0,
                'failing_count': row[5] or 0,
                'passing_rate': round((row[4] or 0) / total * 100, 1) if total > 0 else 0
            }
        return {'total_students': 0, 'average_score': 0, 'min_score': 0, 
                'max_score': 0, 'passing_count': 0, 'failing_count': 0, 'passing_rate': 0}
    
    @staticmethod
    def get_overall_statistics() -> Dict[str, Any]:
        """Get overall system statistics"""
        result = db.execute_query("""
            SELECT 
                COUNT(DISTINCT s.student_id) as total_students,
                COUNT(DISTINCT s.course_id) as total_courses,
                AVG(g.final_score) as avg_score,
                COUNT(CASE WHEN g.final_score >= 60 THEN 1 END) as passing_count,
                COUNT(CASE WHEN g.final_score < 60 THEN 1 END) as failing_count
            FROM students s
            LEFT JOIN grades g ON s.student_id = g.student_id
            WHERE s.status = 'active'
        """)
        
        if result:
            row = result[0]
            total_graded = (row[3] or 0) + (row[4] or 0)
            return {
                'total_students': row[0] or 0,
                'total_courses': row[1] or 0,
                'average_score': round(row[2] or 0, 2),
                'total_graded': total_graded,
                'passing_count': row[3] or 0,
                'failing_count': row[4] or 0,
                'passing_rate': round((row[3] or 0) / total_graded * 100, 1) if total_graded > 0 else 0
            }
        return {}