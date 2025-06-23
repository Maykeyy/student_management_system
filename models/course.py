from database import db

class Course:
    @staticmethod
    def create(name, description):
        query = "INSERT INTO courses (name, description) VALUES (%s, %s)"
        return db.execute_query(query, (name, description))

    @staticmethod
    def get_all():
        return db.fetch_all("SELECT id, name, description FROM courses")

    @staticmethod
    def get_by_id(course_id):
        return db.fetch_one("SELECT id, name, description FROM courses WHERE id = %s", (course_id,))

    @staticmethod
    def update(course_id, name, description):
        query = "UPDATE courses SET name = %s, description = %s WHERE id = %s"
        return db.execute_query(query, (name, description, course_id))

    @staticmethod
    def delete(course_id):
        return db.execute_query("DELETE FROM courses WHERE id = %s", (course_id,))