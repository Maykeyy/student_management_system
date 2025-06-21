# ==============================================================================
# UTILITIES (utils/validators.py)
# ==============================================================================

import re
from typing import Tuple, Optional, List, Any

class InputValidator:
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate student name"""
        name = name.strip()
        if not name:
            return False, "Name cannot be empty"
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        if len(name) > 255:
            return False, "Name cannot exceed 255 characters"
        if not re.match(r"^[a-zA-Z\s\-\'\.]+$", name):
            return False, "Name can only contain letters, spaces, hyphens, apostrophes, and periods"
        return True, name

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email address"""
        if not email:
            return True, ""  # Email is optional

        email = email.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        return True, email

    @staticmethod
    def validate_year_level(year: str) -> Tuple[bool, int]:
        """Validate year level"""
        try:
            year_int = int(year)
            if year_int not in [1, 2, 3, 4]:
                return False, 0
            return True, year_int
        except ValueError:
            return False, 0

    @staticmethod
    def validate_grade(grade: str) -> Tuple[bool, float]:
        """Validate grade (0-100)"""
        try:
            grade_float = float(grade)
            if not (0 <= grade_float <= 100):
                return False, 0.0
            return True, round(grade_float, 2)
        except ValueError:
            return False, 0.0

    @staticmethod
    def validate_weight(weight: str) -> Tuple[bool, float]:
        """Validate weight (0-1)"""
        try:
            weight_float = float(weight)
            if not (0 <= weight_float <= 1):
                return False, 0.0
            return True, round(weight_float, 3)
        except ValueError:
            return False, 0.0

    @staticmethod
    def validate_student_id(student_id: str) -> Tuple[bool, str]:
        """Validate student ID format"""
        student_id = student_id.strip()
        if not student_id:
            return False, "Student ID cannot be empty"
        if not re.match(r'^\d{8}$', student_id):
            return False, "Student ID must be exactly 8 digits"
        return True, student_id


class InputHelper:
    @staticmethod
    def get_validated_input(prompt: str, validator_func, error_msg: str = "Invalid input") -> Any:
        """Get validated input with retry logic"""
        while True:
            user_input = input(prompt).strip()
            is_valid, result = validator_func(user_input)
            if is_valid:
                return result
            print(f"Error: {result if isinstance(result, str) else error_msg}")

    @staticmethod
    def get_choice(prompt: str, valid_choices: List[str]) -> str:
        """Get user choice from valid options"""
        while True:
            choice = input(prompt).strip()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please select from: {', '.join(valid_choices)}")

    @staticmethod
    def confirm_action(message: str) -> bool:
        """Get confirmation for destructive actions"""
        while True:
            response = input(f"{message} (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', '']:
                return False
            print("Please enter 'y' for yes or 'n' for no.")
