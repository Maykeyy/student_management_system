## Requirements (Make sure these 3 is installed in your PC!)

- Python
- VSCode
- XAMPP

## Setup Steps

1. **Install**

   - Navigate to the project folder using CMD `example: cd users/ian/etcetc`
   - Run: `pip install -r requirements.txt` or `python -m pip install -r requirements.txt` or `py -m pip install -r requirements.txt`

2. **Configure MySQL Database**

   - Start XAMPP (Apache + MySQL)
   - Create Database called `lms_db`.
   - Import the file from `database/lms_db.sql` to the database just created.

3. **Run Application**
   - In CMD, run: `python main.py` or `py main.py`

**ADMIN CREDENTIALS TO ACCESS ADMIN SIDE:**

- ID: `000001`
- Password: `admin123`
