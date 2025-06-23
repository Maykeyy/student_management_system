from database import db

class Subject:
    @staticmethod
    def create(code, name, description, teacher_id, course_id):
        query = "INSERT INTO subjects (code, name, description, teacher_id, course_id) VALUES (%s, %s, %s, %s, %s)"
        return db.execute_query(query, (code, name, description, teacher_id, course_id))

    @staticmethod
    def get_by_teacher(teacher_id):
        return db.fetch_all("SELECT s.id, s.code, s.name, s.description, c.name FROM subjects s LEFT JOIN courses c ON s.course_id = c.id WHERE s.teacher_id = %s", (teacher_id,))

    @staticmethod
    def get_all():
        return db.fetch_all("SELECT s.id, s.code, s.name, s.description, t.name, c.name FROM subjects s LEFT JOIN teachers t ON s.teacher_id = t.id LEFT JOIN courses c ON s.course_id = c.id")

    @staticmethod
    def get_by_id(subject_id):
        return db.fetch_one("SELECT id, code, name, description, teacher_id, course_id FROM subjects WHERE id = %s", (subject_id,))

    @staticmethod
    def update(subject_id, code, name, description, course_id):
        query = "UPDATE subjects SET code = %s, name = %s, description = %s, course_id = %s WHERE id = %s"
        return db.execute_query(query, (code, name, description, course_id, subject_id))

    @staticmethod
    def delete(subject_id):
        return db.execute_query("DELETE FROM subjects WHERE id = %s", (subject_id,))

    @staticmethod
    def get_enrolled_by_student(student_id):
        return db.fetch_all("SELECT s.code, s.name, e.status FROM subjects s JOIN enrollments e ON s.id = e.subject_id WHERE e.student_id = %s", (student_id,))