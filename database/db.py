# ==============================================================================
# DATABASE MANAGER (database/db.py)
# ==============================================================================

import mysql.connector
from contextlib import contextmanager
from typing import Dict, List, Optional, Any, Tuple
from config import Config  # Make sure config.py returns DB credentials

class DatabaseManager:
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self._test_connection()

    def _test_connection(self):
        """Test connection during initialization"""
        try:
            conn = mysql.connector.connect(**self.config)
            conn.close()
            print("Database connection successful!")
        except mysql.connector.Error as err:
            print(f"❌ Database connection failed: {err}")
            print("Ensure MySQL server is running and DB exists.")
            import sys
            sys.exit(1)

    @contextmanager
    def get_connection(self):
        """Provide a reusable DB connection context"""
        conn = None
        try:
            conn = mysql.connector.connect(**self.config)
            yield conn
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {err}")
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        """Execute SELECT queries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_update(self, query: str, params: Tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount

    def get_last_insert_id(self, query: str, params: Tuple = None) -> int:
        """Insert and return last inserted ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid

    def setup_schema(self):
        """Schema setup is skipped since tables already exist"""
        print("✔ Tables already created manually — skipping setup.")


# ✅ Global instance of DB Manager
db = DatabaseManager(Config.get_db_config())
