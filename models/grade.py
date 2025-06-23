from database import db

class Grade:
    @staticmethod
    def create_or_update(enrollment_id, grade, remarks):
        existing = db.fetch_one("SELECT id FROM grades WHERE enrollment_id = %s", (enrollment_id,))
        if existing:
            query = "UPDATE grades SET grade = %s, remarks = %s WHERE enrollment_id = %s"
            return db.execute_query(query, (grade, remarks, enrollment_id))
        else:
            query = "INSERT INTO grades (enrollment_id, grade, remarks) VALUES (%s, %s, %s)"
            return db.execute_query(query, (enrollment_id, grade, remarks))

    @staticmethod
    def get_by_student(student_id):
        query = """SELECT s.code, s.name, g.grade, g.remarks 
                   FROM grades g 
                   JOIN enrollments e ON g.enrollment_id = e.id 
                   JOIN subjects s ON e.subject_id = s.id 
                   WHERE e.student_id = %s AND e.status = 'approved'"""
        return db.fetch_all(query, (student_id,))

    @staticmethod
    def get_by_enrollment(enrollment_id):
        return db.fetch_one("SELECT grade, remarks FROM grades WHERE enrollment_id = %s", (enrollment_id,))