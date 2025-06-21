# ==============================================================================
# UTILITIES (utils/display.py)
# ==============================================================================

from typing import List, Any, Dict
import math
from models.student import Student
from models.grade import Grade


class DisplayHelper:
    @staticmethod
    def print_header(title: str, width: int = 80, char: str = "="):
        """Print formatted header"""
        print(f"\n{title.center(width, char)}")

    @staticmethod
    def print_subheader(title: str, width: int = 80, char: str = "-"):
        """Print formatted subheader"""
        print(f"{title.center(width, char)}")

    @staticmethod
    def print_table(headers: List[str], rows: List[List[Any]], max_width: int = 120):
        """Print formatted table with proper column alignment"""
        if not rows:
            print("No data to display.")
            return

        # Calculate column widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))

        # Adjust widths if total exceeds max_width
        total_width = sum(widths) + (len(headers) - 1) * 3
        if total_width > max_width:
            scale = (max_width - (len(headers) - 1) * 3) / sum(widths)
            widths = [max(8, int(w * scale)) for w in widths]

        # Print header
        header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        separator = "-+-".join("-" * widths[i] for i in range(len(headers)))

        print("\n" + header_line)
        print(separator)

        # Print rows
        for row in rows:
            formatted_row = []
            for i, cell in enumerate(row):
                if i < len(widths):
                    cell_str = str(cell)
                    if len(cell_str) > widths[i]:
                        cell_str = cell_str[:widths[i]-3] + "..."
                    formatted_row.append(cell_str.ljust(widths[i]))
            print(" | ".join(formatted_row))

    @staticmethod
    def print_student_list(students: List[Student], show_grades: bool = False):
        """Print formatted student list"""
        if not students:
            print("No students found.")
            return

        if show_grades:
            headers = ["ID", "Name", "Course", "Year", "Quiz", "Activity", "Exam", "Final", "Grade"]
            rows = []
            for student in students:
                grade = Grade.find_by_student_id(student.student_id)
                if grade:
                    rows.append([
                        student.student_id, student.full_name, student.course_code,
                        student.year_level, grade.quiz, grade.activity, grade.exam,
                        grade.final_score or "N/A", grade.letter_grade or "N/A"
                    ])
                else:
                    rows.append([
                        student.student_id, student.full_name, student.course_code,
                        student.year_level, "N/A", "N/A", "N/A", "N/A", "N/A"
                    ])
        else:
            headers = ["ID", "Name", "Course", "Year", "Email", "Status"]
            rows = [[s.student_id, s.full_name, s.course_code, s.year_level,
                    s.email or "N/A", s.status] for s in students]

        DisplayHelper.print_table(headers, rows)

    @staticmethod
    def print_grade_report(grades: List[Grade]):
        """Print formatted grade report"""
        if not grades:
            print("No grades found.")
            return

        headers = ["Rank", "ID", "Name", "Course", "Quiz", "Activity", "Exam", "Final", "Grade"]
        rows = []
        for i, grade in enumerate(grades, 1):
            rows.append([
                i, grade.student_id, grade.student_name, grade.course_code,
                grade.quiz, grade.activity, grade.exam,
                grade.final_score or "N/A", grade.letter_grade or "N/A"
            ])

        DisplayHelper.print_table(headers, rows)

    @staticmethod
    def print_statistics(stats: Dict[str, Any], title: str = "Statistics"):
        """Print formatted statistics"""
        DisplayHelper.print_subheader(title)
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            print(f"{formatted_key:.<30} {value}")
        print()
