from datetime import datetime
from app.utils.db import get_db_connection
from app.utils.logger import logger

class FeeService:
    @staticmethod
    def add_fee(student_id, amount, date):
        try:
            student_id = int(student_id)
        except ValueError:
            return False, "Validation Error: Student ID must be an integer."

        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Validation Error: Fee amount must be greater than 0."
        except ValueError:
            return False, "Validation Error: Fee amount must be a valid number."

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False, "Validation Error: Invalid date format. Use YYYY-MM-DD."

        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            
            query = "INSERT INTO fees (student_id, amount, date) VALUES (?, ?, ?)"
            cursor.execute(query, (student_id, amount, date))
            conn.commit()
            return True, "Fee added successfully"
        except Exception as e:
            logger.error(f"Error adding fee: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_fees():
        try:
            conn = get_db_connection()
            if not conn: return []
            cursor = conn.cursor()
            query = """
            SELECT f.id, s.name as student_name, f.amount, f.date 
            FROM fees f 
            JOIN students s ON f.student_id = s.id
            ORDER BY f.date DESC
            """
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching fees: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_total_fees():
        try:
            conn = get_db_connection()
            if not conn: return 0.0
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM fees")
            result = cursor.fetchone()[0]
            return float(result) if result else 0.0
        except Exception as e:
            logger.error(f"Error getting total fees: {e}")
            return 0.0
        finally:
            if 'cursor' in locals() and cursor: cursor.close()
