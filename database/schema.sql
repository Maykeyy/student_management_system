
-- Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    credits INT DEFAULT 3,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id CHAR(8) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    course_id INT NOT NULL,
    year_level TINYINT CHECK (year_level BETWEEN 1 AND 4),
    status ENUM('active', 'inactive', 'graduated') DEFAULT 'active',
    enrollment_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
) ENGINE=InnoDB;

-- Grade Settings Table (uses DECIMAL instead of FLOAT to support accurate constraint)
CREATE TABLE IF NOT EXISTS grade_settings (
    id INT PRIMARY KEY DEFAULT 1,
    quiz_weight DECIMAL(5,4) DEFAULT 0.3000,
    activity_weight DECIMAL(5,4) DEFAULT 0.3000,
    exam_weight DECIMAL(5,4) DEFAULT 0.4000,
    passing_grade DECIMAL(5,2) DEFAULT 60.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (quiz_weight + activity_weight + exam_weight = 1.0000)
) ENGINE=InnoDB;

-- Grades Table (no subquery in generated column; calculated externally)
CREATE TABLE IF NOT EXISTS grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id CHAR(8) NOT NULL,
    quiz FLOAT DEFAULT 0,
    activity FLOAT DEFAULT 0,
    exam FLOAT DEFAULT 0,
    final_score FLOAT DEFAULT 0, -- manually calculated in app or via trigger
    letter_grade CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Grade Audit Log
CREATE TABLE IF NOT EXISTS grade_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id CHAR(8) NOT NULL,
    grade_type ENUM('quiz', 'activity', 'exam') NOT NULL,
    old_value FLOAT,
    new_value FLOAT,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
) ENGINE=InnoDB;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'registrar') DEFAULT 'teacher',
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


