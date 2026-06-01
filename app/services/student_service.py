import re
from app.utils.db import get_db_connection
from app.models.student_model import Student
from app.utils.logger import logger

class StudentService:
    @staticmethod
    def add_student(name, student_class, age):
        if not name or len(str(name).strip()) < 2:
            return False, "Validation Error: Name must be at least 2 characters long."
        if not re.match(r"^[a-zA-Z\s.]+$", str(name)):
            return False, "Validation Error: Name can only contain letters, spaces, and dots."
            
        if not student_class or not str(student_class).strip():
            return False, "Validation Error: Class cannot be empty."
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", str(student_class)):
            return False, "Validation Error: Class contains invalid characters."
        try:
            age = int(age)
            if age < 3 or age > 100:
                return False, "Validation Error: Age must be between 3 and 100."
        except ValueError:
            return False, "Validation Error: Age must be a valid number."

        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "INSERT INTO students (name, class, age) VALUES (?, ?, ?)"
            cursor.execute(query, (name, student_class, age))
            conn.commit()
            return True, "Student added successfully"
        except Exception as e:
            logger.error(f"Error adding student: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_all_students():
        try:
            conn = get_db_connection()
            if not conn: return []
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, class, age FROM students")
            results = cursor.fetchall()
            return [Student(row[0], row[1], row[2], row[3]) for row in results]
        except Exception as e:
            logger.error(f"Error fetching students: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def update_student(student_id, name, student_class, age):
        if not name or len(str(name).strip()) < 2:
            return False, "Validation Error: Name must be at least 2 characters long."
        if not re.match(r"^[a-zA-Z\s.]+$", str(name)):
            return False, "Validation Error: Name can only contain letters, spaces, and dots."
            
        if not student_class or not str(student_class).strip():
            return False, "Validation Error: Class cannot be empty."
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", str(student_class)):
            return False, "Validation Error: Class contains invalid characters."
        try:
            age = int(age)
            if age < 3 or age > 100:
                return False, "Validation Error: Age must be between 3 and 100."
        except ValueError:
            return False, "Validation Error: Age must be a valid number."

        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "UPDATE students SET name=?, class=?, age=? WHERE id=?"
            cursor.execute(query, (name, student_class, age, student_id))
            conn.commit()
            return True, "Student updated successfully"
        except Exception as e:
            logger.error(f"Error updating student: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def delete_student(student_id):
        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "DELETE FROM students WHERE id=?"
            cursor.execute(query, (student_id,))
            conn.commit()
            return True, "Student deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting student: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_total_students():
        try:
            conn = get_db_connection()
            if not conn: return 0
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting total students: {e}")
            return 0
        finally:
            if 'cursor' in locals() and cursor: cursor.close()
