from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.attendance_service import AttendanceService
from app.services.fee_service import FeeService

web_bp = Blueprint('web', __name__)

# Authentication Wrapper
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if AuthService.login(username, password)[0]:
            session['user'] = username
            return redirect(url_for('web.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@web_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('web.login'))

@web_bp.route('/')
@web_bp.route('/dashboard')
@login_required
def dashboard():
    from datetime import datetime
    total_students = StudentService.get_total_students()
    total_teachers = TeacherService.get_total_teachers()
    total_fees = FeeService.get_total_fees()
    now = datetime.now().strftime('%B %d, %Y')
    return render_template('dashboard.html', 
                         total_students=total_students, 
                         total_teachers=total_teachers, 
                         total_fees=total_fees,
                         now=now)

# Students Routes
@web_bp.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name')
            cls = request.form.get('class')
            age = request.form.get('age')
            success, msg = StudentService.add_student(name, cls, age)
            flash(msg, 'success' if success else 'danger')
        elif action == 'delete':
            student_id = request.form.get('student_id')
            success, msg = StudentService.delete_student(student_id)
            flash(msg, 'success' if success else 'danger')
        elif action == 'update':
            student_id = request.form.get('student_id')
            name = request.form.get('name')
            cls = request.form.get('class')
            age = request.form.get('age')
            success, msg = StudentService.update_student(student_id, name, cls, age)
            flash(msg, 'success' if success else 'danger')
        return redirect(url_for('web.students'))
    
    student_list = StudentService.get_all_students()
    return render_template('students.html', students=student_list)

# Teachers Routes
@web_bp.route('/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name')
            subject = request.form.get('subject')
            success, msg = TeacherService.add_teacher(name, subject)
            flash(msg, 'success' if success else 'danger')
        elif action == 'delete':
            teacher_id = request.form.get('teacher_id')
            success, msg = TeacherService.delete_teacher(teacher_id)
            flash(msg, 'success' if success else 'danger')
        elif action == 'update':
            teacher_id = request.form.get('teacher_id')
            name = request.form.get('name')
            subject = request.form.get('subject')
            success, msg = TeacherService.update_teacher(teacher_id, name, subject)
            flash(msg, 'success' if success else 'danger')
        return redirect(url_for('web.teachers'))
    
    teacher_list = TeacherService.get_all_teachers()
    return render_template('teachers.html', teachers=teacher_list)

# Attendance Routes
@web_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        date = request.form.get('date')
        status = request.form.get('status')
        success, msg = AttendanceService.mark_attendance(student_id, date, status)
        flash(msg, 'success' if success else 'danger')
        return redirect(url_for('web.attendance'))
        
    records = AttendanceService.get_attendance()
    students = StudentService.get_all_students()
    return render_template('attendance.html', records=records, students=students)

# Fees Routes
@web_bp.route('/fees', methods=['GET', 'POST'])
@login_required
def fees():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        amount = request.form.get('amount')
        date = request.form.get('date')
        success, msg = FeeService.add_fee(student_id, amount, date)
        flash(msg, 'success' if success else 'danger')
        return redirect(url_for('web.fees'))
        
    records = FeeService.get_fees()
    students = StudentService.get_all_students()
    return render_template('fees.html', records=records, students=students)
