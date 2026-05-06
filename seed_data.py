from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.attendance_service import AttendanceService
from app.utils.logger import logger
from datetime import datetime

def seed_data():
    logger.info("Starting data seed...")

    # Add Teachers with Pakistani names
    teachers = [
        ("Ahmed Raza", "Mathematics"),
        ("Sana Ibrahim", "Physics"),
        ("Tariq Mahmood", "Computer Science")
    ]
    for name, subject in teachers:
        StudentService.add_student  # Just importing to ensure connection setup
        TeacherService.add_teacher(name, subject)
        logger.info(f"Added teacher: {name}")

    # Add Students with Pakistani names
    students = [
        ("Ali Khan", "10th", 15),
        ("Fatima Tariq", "10th", 15),
        ("Usman Ahmed", "9th", 14),
        ("Ayesha Bilal", "9th", 14),
        ("Hamza Shah", "11th", 16)
    ]
    
    # We need to capture the generated IDs to mark attendance.
    # Since add_student doesn't return the ID, we'll fetch all students after adding
    for name, s_class, age in students:
        StudentService.add_student(name, s_class, age)
        logger.info(f"Added student: {name}")

    # Fetch students to mark attendance
    all_students = StudentService.get_all_students()
    
    today = datetime.now().strftime('%Y-%m-%d')
    for s in all_students:
        # Mark present for most, absent for one
        status = "Present" if s.name != "Usman Ahmed" else "Absent"
        AttendanceService.mark_attendance(s.id, today, status)
        logger.info(f"Marked attendance for {s.name}: {status}")

    logger.info("Data seeding complete!")

if __name__ == "__main__":
    seed_data()
