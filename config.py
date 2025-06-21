class Config:
    # Database Configuration (no .env dependency)
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'student_management'
    
    # Application Settings
    APP_NAME = "Student Management System"
    APP_VERSION = "2.0.0"
    
    # Grade Settings (defaults)
    DEFAULT_QUIZ_WEIGHT = 0.30
    DEFAULT_ACTIVITY_WEIGHT = 0.30
    DEFAULT_EXAM_WEIGHT = 0.40
    DEFAULT_PASSING_GRADE = 60.0
    
    # Display Settings
    TABLE_MAX_WIDTH = 120
    HEADER_WIDTH = 80
    
    @classmethod
    def get_db_config(cls):
        return {
            'host': cls.DB_HOST,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'database': cls.DB_NAME
        }