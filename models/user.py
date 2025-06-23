# models/user.py:
import random
from database import db

class User:
    @staticmethod
    def generate_id():
        while True:
            user_id = str(random.randint(100000, 999999))
            if not User.id_exists(user_id):
                return user_id

    @staticmethod
    def id_exists(user_id):
        tables = ['admins', 'teachers', 'students']
        for table in tables:
            result = db.fetch_one(f"SELECT user_id FROM {table} WHERE user_id = %s", (user_id,))
            if result:
                return True
        return False

    @staticmethod
    def authenticate(user_id, password):
        tables = [('admins', 'admin'), ('teachers', 'teacher'), ('students', 'student')]
        for table, role in tables:
            result = db.fetch_one(f"SELECT id, name FROM {table} WHERE user_id = %s AND password = %s", (user_id, password))
            if result:
                return {'id': result[0], 'name': result[1], 'role': role, 'user_id': user_id}
        return None

class Admin:
    @staticmethod
    def create_teacher(name, email, password, position):
        user_id = User.generate_id()
        query = "INSERT INTO teachers (user_id, name, email, password, position) VALUES (%s, %s, %s, %s, %s)"
        return db.execute_query(query, (user_id, name, email, password, position))

    @staticmethod
    def create_student(name, email, password, course_id, year_level):
        user_id = User.generate_id()
        query = "INSERT INTO students (user_id, name, email, password, course_id, year_level) VALUES (%s, %s, %s, %s, %s, %s)"
        return db.execute_query(query, (user_id, name, email, password, course_id, year_level))

    @staticmethod
    def get_teachers():
        return db.fetch_all("SELECT id, user_id, name, email, position FROM teachers")

    @staticmethod
    def get_students():
        return db.fetch_all("SELECT s.id, s.user_id, s.name, s.email, c.name, s.year_level FROM students s LEFT JOIN courses c ON s.course_id = c.id")

    @staticmethod
    def update_teacher(user_id, name, email, password, position):
        query = "UPDATE teachers SET name = %s, email = %s, password = %s, position = %s WHERE user_id = %s"
        return db.execute_query(query, (name, email, password, position, user_id))

    @staticmethod
    def update_student(user_id, name, email, password, course_id, year_level):
        query = "UPDATE students SET name = %s, email = %s, password = %s, course_id = %s, year_level = %s WHERE user_id = %s"
        return db.execute_query(query, (name, email, password, course_id, year_level, user_id))

    @staticmethod
    def delete_teacher(user_id):
        return db.execute_query("DELETE FROM teachers WHERE user_id = %s", (user_id,))

    @staticmethod
    def delete_student(user_id):
        return db.execute_query("DELETE FROM students WHERE user_id = %s", (user_id,))

class Teacher:
    @staticmethod
    def get_by_user_id(user_id):
        return db.fetch_one("SELECT id, name FROM teachers WHERE user_id = %s", (user_id,))

class Student:
    @staticmethod
    def get_by_user_id(user_id):
        return db.fetch_one("SELECT s.id, s.name, c.name, s.year_level FROM students s LEFT JOIN courses c ON s.course_id = c.id WHERE s.user_id = %s", (user_id,))