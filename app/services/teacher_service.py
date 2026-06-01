import re
from app.utils.db import get_db_connection
from app.models.teacher_model import Teacher
from app.utils.logger import logger


class TeacherService:

    # ─────────────────────────── helpers ────────────────────────────

    @staticmethod
    def _validate_name(name: str):
        if not isinstance(name, str):
            return False, "Validation Error: Name must be a text value."

        name = name.strip()

        if len(name) < 2:
            return False, "Validation Error: Teacher name must be at least 2 characters long."
        if len(name) > 60:
            return False, "Validation Error: Teacher name must not exceed 60 characters."

        if not re.match(r"^[a-zA-Z][a-zA-Z\s.]*$", name):
            return False, "Validation Error: Name can only contain letters, spaces, and dots, and must start with a letter."

        if not re.search(r"[a-zA-Z]{2,}", name.replace(" ", "").replace(".", "")):
            return False, "Validation Error: Name must contain at least two actual letters."

        name = re.sub(r"\s{2,}", " ", name)
        return True, name

    @staticmethod
    def _validate_subject(subject: str):
        if not isinstance(subject, str):
            return False, "Validation Error: Subject must be a text value."

        subject = subject.strip()

        if len(subject) < 2:
            return False, "Validation Error: Subject must be at least 2 characters long."
        if len(subject) > 80:
            return False, "Validation Error: Subject must not exceed 80 characters."

        if not re.match(r"^[a-zA-Z][a-zA-Z0-9\s\-]*$", subject):
            return False, "Validation Error: Subject must start with a letter and may only contain letters, digits, spaces, and hyphens."

        subject = re.sub(r"\s{2,}", " ", subject)
        return True, subject

    @staticmethod
    def _validate_id(teacher_id):
        try:
            tid = int(teacher_id)
            if tid <= 0:
                raise ValueError
            return True, tid
        except (ValueError, TypeError):
            return False, "Validation Error: Teacher ID must be a positive integer."

    # ─────────────────────────── public API ─────────────────────────

    @staticmethod
    def add_teacher(name, subject):
        ok, result = TeacherService._validate_name(name)
        if not ok:
            return False, result
        name = result

        ok, result = TeacherService._validate_subject(subject)
        if not ok:
            return False, result
        subject = result

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return False, "DB Connection Error"

            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM teachers WHERE LOWER(name) = LOWER(?) AND LOWER(subject) = LOWER(?)",
                (name, subject)
            )
            if cursor.fetchone():
                return False, "Validation Error: A teacher with this name and subject already exists."

            cursor.execute(
                "INSERT INTO teachers (name, subject) VALUES (?, ?)",
                (name, subject)
            )
            conn.commit()
            return True, "Teacher added successfully."

        except Exception as e:
            logger.error(f"Error adding teacher: {e}")
            return False, "An unexpected error occurred while adding the teacher."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_all_teachers():
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return []

            cursor = conn.cursor()
            cursor.execute("SELECT id, name, subject FROM teachers ORDER BY name ASC")
            results = cursor.fetchall()
            return [Teacher(row[0], row[1], row[2]) for row in results]

        except Exception as e:
            logger.error(f"Error fetching teachers: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def update_teacher(teacher_id, name, subject):
        ok, result = TeacherService._validate_id(teacher_id)
        if not ok:
            return False, result
        teacher_id = result

        ok, result = TeacherService._validate_name(name)
        if not ok:
            return False, result
        name = result

        ok, result = TeacherService._validate_subject(subject)
        if not ok:
            return False, result
        subject = result

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return False, "DB Connection Error"

            cursor = conn.cursor()

            cursor.execute("SELECT id FROM teachers WHERE id = ?", (teacher_id,))
            if not cursor.fetchone():
                return False, f"Validation Error: No teacher found with ID {teacher_id}."

            cursor.execute(
                "SELECT id FROM teachers WHERE LOWER(name) = LOWER(?) AND LOWER(subject) = LOWER(?) AND id != ?",
                (name, subject, teacher_id)
            )
            if cursor.fetchone():
                return False, "Validation Error: Another teacher with this name and subject already exists."

            cursor.execute(
                "UPDATE teachers SET name = ?, subject = ? WHERE id = ?",
                (name, subject, teacher_id)
            )
            conn.commit()
            return True, "Teacher updated successfully."

        except Exception as e:
            logger.error(f"Error updating teacher: {e}")
            return False, "An unexpected error occurred while updating the teacher."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def delete_teacher(teacher_id):
        ok, result = TeacherService._validate_id(teacher_id)
        if not ok:
            return False, result
        teacher_id = result

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return False, "DB Connection Error"

            cursor = conn.cursor()

            cursor.execute("SELECT id FROM teachers WHERE id = ?", (teacher_id,))
            if not cursor.fetchone():
                return False, f"Validation Error: No teacher found with ID {teacher_id}."

            cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
            conn.commit()
            return True, "Teacher deleted successfully."

        except Exception as e:
            logger.error(f"Error deleting teacher: {e}")
            return False, "An unexpected error occurred while deleting the teacher."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_total_teachers():
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if not conn:
                return 0

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            row = cursor.fetchone()
            return row[0] if row else 0

        except Exception as e:
            logger.error(f"Error getting total teachers: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
