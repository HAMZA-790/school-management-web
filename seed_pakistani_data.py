from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.services.fee_service import FeeService
from app.utils.logger import logger
from datetime import datetime

def seed_pakistani_data():
    logger.info("Seeding Pakistani student records...")

    # Students with Pakistani names
    students_data = [
        ("Muhammad Ali", "10th", 15),
        ("Fatima Zahra", "9th", 14),
        ("Zeeshan Haider", "11th", 16),
        ("Sana Khan", "10th", 15),
        ("Bilal Ahmed", "8th", 13)
    ]

    for name, cls, age in students_data:
        success, msg = StudentService.add_student(name, cls, age)
        if success:
            logger.info(f"Added student: {name}")
        else:
            logger.error(f"Failed to add student {name}: {msg}")

    # Fetch added students to use their IDs
    all_students = StudentService.get_all_students()
    pak_students = [s for s in all_students if s.name in [d[0] for d in students_data]]

    today = datetime.now().strftime('%Y-%m-%d')
    
    # Add Attendance and Fees
    for s in pak_students:
        # Mark Attendance
        status = "Present" if s.name != "Bilal Ahmed" else "Absent"
        AttendanceService.mark_attendance(s.id, today, status)
        logger.info(f"Marked attendance for {s.name}: {status}")

        # Add Fee Record
        amount = 5000.0 if "1" in s.student_class else 3000.0
        FeeService.add_fee(s.id, amount, today)
        logger.info(f"Added fee for {s.name}: {amount}")

    logger.info("Pakistani data seeding complete!")

if __name__ == "__main__":
    import os
    if not os.getenv("DB_TYPE"):
        os.environ["DB_TYPE"] = "sqlite"
    seed_pakistani_data()
