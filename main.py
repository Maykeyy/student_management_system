import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.cli import StudentManagementCLI
from services.student_service import StudentService
from services.grading_service import GradingService 

if __name__ == '__main__':
    try:
        app = StudentManagementCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("Please contact support or check system configuration.")
        sys.exit(1)
