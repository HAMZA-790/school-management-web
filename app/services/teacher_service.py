from app.utils.db import get_db_connection
from app.models.teacher_model import Teacher
from app.utils.logger import logger

class TeacherService:
    @staticmethod
    def add_teacher(name, subject):
        if not name or len(str(name).strip()) < 2:
            return False, "Validation Error: Teacher name must be at least 2 characters long."
        if not subject or not str(subject).strip():
            return False, "Validation Error: Subject cannot be empty."

        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "INSERT INTO teachers (name, subject) VALUES (?, ?)"
            cursor.execute(query, (name, subject))
            conn.commit()
            return True, "Teacher added successfully"
        except Exception as e:
            logger.error(f"Error adding teacher: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_all_teachers():
        try:
            conn = get_db_connection()
            if not conn: return []
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, subject FROM teachers")
            results = cursor.fetchall()
            return [Teacher(row[0], row[1], row[2]) for row in results]
        except Exception as e:
            logger.error(f"Error fetching teachers: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def update_teacher(teacher_id, name, subject):
        if not name or len(str(name).strip()) < 2:
            return False, "Validation Error: Teacher name must be at least 2 characters long."
        if not subject or not str(subject).strip():
            return False, "Validation Error: Subject cannot be empty."

        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "UPDATE teachers SET name=?, subject=? WHERE id=?"
            cursor.execute(query, (name, subject, teacher_id))
            conn.commit()
            return True, "Teacher updated successfully"
        except Exception as e:
            logger.error(f"Error updating teacher: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def delete_teacher(teacher_id):
        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            query = "DELETE FROM teachers WHERE id=?"
            cursor.execute(query, (teacher_id,))
            conn.commit()
            return True, "Teacher deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting teacher: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_total_teachers():
        try:
            conn = get_db_connection()
            if not conn: return 0
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting total teachers: {e}")
            return 0
        finally:
            if 'cursor' in locals() and cursor: cursor.close()
