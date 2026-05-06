import sqlite3
import os
from app.utils.logger import logger

def setup_sqlite_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sqlite_db_path = os.path.join(base_dir, "school_db.sqlite")
    
    try:
        connection = sqlite3.connect(sqlite_db_path)
        cursor = connection.cursor()
        
        # Create Tables
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username VARCHAR(50) NOT NULL UNIQUE,
              password VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS students (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name VARCHAR(100) NOT NULL,
              class VARCHAR(50) NOT NULL,
              age INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS teachers (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name VARCHAR(100) NOT NULL,
              subject VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS attendance (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              student_id INTEGER NOT NULL,
              date DATE NOT NULL,
              status VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent', 'Late')),
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS fees (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              student_id INTEGER NOT NULL,
              amount DECIMAL(10,2) NOT NULL,
              date DATE NOT NULL,
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
            """
        ]

        for table_query in tables:
            cursor.execute(table_query)
        
        logger.info("SQLite tables checked/created successfully.")

        # Insert Sample Data
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpassword')")
        
        # Check if students exist
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO students (name, class, age) VALUES ('John Doe', '10th', 15), ('Jane Smith', '9th', 14)")
            
        # Check if teachers exist
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO teachers (name, subject) VALUES ('Mr. Anderson', 'Math'), ('Mrs. Davis', 'Science')")

        connection.commit()
        logger.info("SQLite sample data checked/inserted successfully.")

    except sqlite3.Error as e:
        logger.error(f"Error while connecting to SQLite: {e}")
    finally:
        if 'connection' in locals():
            try:
                connection.close()
                logger.info("SQLite connection is closed")
            except sqlite3.Error:
                pass

if __name__ == "__main__":
    setup_sqlite_database()
