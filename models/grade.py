from database import db

class Grade:
    @staticmethod
    def create_or_update(enrollment_id, grade=None, remarks=None, activity_score=None, quiz_score=None, exam_score=None, activity_weight=40.0, quiz_weight=20.0, exam_weight=40.0, is_component_based=False):
        """
        Create or update a grade entry. Supports both legacy single-grade and new component-based grading.
        """
        existing = db.fetch_one("SELECT id FROM grades WHERE enrollment_id = %s", (enrollment_id,))
        
        # Calculate final grade and remarks for component-based grading
        final_grade = None
        computed_remarks = remarks
        
        if is_component_based and activity_score is not None and quiz_score is not None and exam_score is not None:
            # Ensure weights sum to 100
            total_weight = activity_weight + quiz_weight + exam_weight
            if total_weight != 100:
                activity_weight = activity_weight * (100 / total_weight)
                quiz_weight = quiz_weight * (100 / total_weight)
                exam_weight = exam_weight * (100 / total_weight)
            
            final_grade = (activity_score * activity_weight / 100) + (quiz_score * quiz_weight / 100) + (exam_score * exam_weight / 100)
            computed_remarks = "Passed" if final_grade >= 75 else "Failed"
        
        if existing:
            if is_component_based:
                query = """UPDATE grades SET 
                          activity_score = %s, quiz_score = %s, exam_score = %s,
                          activity_weight = %s, quiz_weight = %s, exam_weight = %s,
                          final_grade = %s, remarks = %s, is_component_based = %s 
                          WHERE enrollment_id = %s"""
                return db.execute_query(query, (activity_score, quiz_score, exam_score, 
                                              activity_weight, quiz_weight, exam_weight,
                                              final_grade, computed_remarks, is_component_based, enrollment_id))
            else:
                query = "UPDATE grades SET grade = %s, remarks = %s WHERE enrollment_id = %s"
                return db.execute_query(query, (grade, remarks, enrollment_id))
        else:
            if is_component_based:
                query = """INSERT INTO grades (enrollment_id, activity_score, quiz_score, exam_score,
                          activity_weight, quiz_weight, exam_weight, final_grade, remarks, is_component_based) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                return db.execute_query(query, (enrollment_id, activity_score, quiz_score, exam_score,
                                              activity_weight, quiz_weight, exam_weight, 
                                              final_grade, computed_remarks, is_component_based))
            else:
                query = "INSERT INTO grades (enrollment_id, grade, remarks) VALUES (%s, %s, %s)"
                return db.execute_query(query, (enrollment_id, grade, remarks))

    @staticmethod
    def get_by_student(student_id):
        """Get all grades for a student with component breakdown"""
        query = """SELECT s.code, s.name, g.grade, g.remarks, g.activity_score, g.quiz_score, 
                   g.exam_score, g.activity_weight, g.quiz_weight, g.exam_weight, 
                   g.final_grade, g.is_component_based
                   FROM grades g 
                   JOIN enrollments e ON g.enrollment_id = e.id 
                   JOIN subjects s ON e.subject_id = s.id 
                   WHERE e.student_id = %s AND e.status = 'approved'"""
        return db.fetch_all(query, (student_id,))

    @staticmethod
    def get_by_enrollment(enrollment_id):
        """Get grade details for a specific enrollment"""
        query = """SELECT grade, remarks, activity_score, quiz_score, exam_score,
                   activity_weight, quiz_weight, exam_weight, final_grade, is_component_based
                   FROM grades WHERE enrollment_id = %s"""
        return db.fetch_one(query, (enrollment_id,))

    @staticmethod
    def get_detailed_by_enrollment(enrollment_id):
        """Get detailed grade information for display"""
        result = Grade.get_by_enrollment(enrollment_id)
        if not result:
            return None
        
        grade_data = {
            'legacy_grade': result[0],
            'remarks': result[1],
            'activity_score': result[2],
            'quiz_score': result[3],
            'exam_score': result[4],
            'activity_weight': result[5],
            'quiz_weight': result[6],
            'exam_weight': result[7],
            'final_grade': result[8],
            'is_component_based': result[9]
        }
        
        return grade_data

    @staticmethod
    def calculate_final_grade(activity_score, quiz_score, exam_score, activity_weight=40.0, quiz_weight=20.0, exam_weight=40.0):
        """Utility method to calculate final grade"""
        if activity_score is None or quiz_score is None or exam_score is None:
            return None
        
        # Normalize weights to sum to 100
        total_weight = activity_weight + quiz_weight + exam_weight
        if total_weight != 100:
            activity_weight = activity_weight * (100 / total_weight)
            quiz_weight = quiz_weight * (100 / total_weight)
            exam_weight = exam_weight * (100 / total_weight)
        
        return (activity_score * activity_weight / 100) + (quiz_score * quiz_weight / 100) + (exam_score * exam_weight / 100)

    @staticmethod
    def get_grade_statistics():
        """Get overall grade statistics"""
        query = """SELECT 
                   COUNT(*) as total_grades,
                   AVG(CASE WHEN is_component_based = 1 THEN final_grade ELSE grade END) as avg_grade,
                   COUNT(CASE WHEN is_component_based = 1 AND final_grade >= 75 THEN 1 
                             WHEN is_component_based = 0 AND grade >= 75 THEN 1 END) as passed_count,
                   COUNT(CASE WHEN is_component_based = 1 AND final_grade < 75 THEN 1 
                             WHEN is_component_based = 0 AND grade < 75 THEN 1 END) as failed_count
                   FROM grades WHERE (grade IS NOT NULL OR final_grade IS NOT NULL)"""
        return db.fetch_one(query)