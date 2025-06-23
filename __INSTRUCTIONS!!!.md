## Requirements

- Python 3.7+
- XAMPP
- pip (Python package manager)

## Setup Steps

1. **Install**

   ```bash
   navigate to the main project folder using CMD, then run the command below:
   --> pip install -r requirements.txt <--
   ```

2. **Configure MySQL Database**

   - Start XAMPP
   - Create Database called `lms_db`.
   - Import the Queries `database/lms_db.sql` to the database just created to be able to create the tables.

3. **Run Application**
   - Go to CMD and run this the command below:
   ```bash
   python main.py
   ```

**Admin CREDENTIAL:**

- ID: `000001`
- Password: `admin123`
