from database import db

class Enrollment:
    @staticmethod
    def create(student_id, subject_id):
        query = "INSERT INTO enrollments (student_id, subject_id) VALUES (%s, %s)"
        return db.execute_query(query, (student_id, subject_id))

    @staticmethod
    def get_pending_by_teacher(teacher_id):
        query = """SELECT e.id, st.name, s.code, s.name, e.enrolled_at 
                   FROM enrollments e 
                   JOIN students st ON e.student_id = st.id 
                   JOIN subjects s ON e.subject_id = s.id 
                   WHERE s.teacher_id = %s AND e.status = 'pending'"""
        return db.fetch_all(query, (teacher_id,))

    @staticmethod
    def update_status(enrollment_id, status):
        query = "UPDATE enrollments SET status = %s WHERE id = %s"
        return db.execute_query(query, (status, enrollment_id))

    @staticmethod
    def get_approved_by_teacher(teacher_id):
        query = """SELECT e.id, st.name, s.code, s.name 
                   FROM enrollments e 
                   JOIN students st ON e.student_id = st.id 
                   JOIN subjects s ON e.subject_id = s.id 
                   WHERE s.teacher_id = %s AND e.status = 'approved'"""
        return db.fetch_all(query, (teacher_id,))

    @staticmethod
    def get_by_student(student_id):
        query = """SELECT e.id, s.code, s.name, e.status 
                   FROM enrollments e 
                   JOIN subjects s ON e.subject_id = s.id 
                   WHERE e.student_id = %s"""
        return db.fetch_all(query, (student_id,))