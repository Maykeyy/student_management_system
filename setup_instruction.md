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
   - Import the MySQL Queries to the Xampp from the `database/schema.sql` to be able to create the database and tables.
   - Update database credentials in `database/connection.py`:

3. **Run Application**
   ```bash
   python main.py
   ```

**Admin CREDENTIAL:**

- ID: `000001`
- Password: `admin123`
