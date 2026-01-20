from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from forms import AdminLoginForm, StudentLoginForm, StaffLoginForm
from models import Admin, Student, Staff
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

# Admin login (username + password)
@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session.clear()
            session['role'] = 'admin'
            session['admin_id'] = admin.id
            session['admin_name'] = admin.name or admin.username
            flash('Logged in as admin', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        flash('Invalid username/password', 'danger')
    return render_template('login_admin.html', form=form)

# Student login (USN only)
@auth_bp.route('/login/student', methods=['GET', 'POST'])
def login_student():
    form = StudentLoginForm()
    if form.validate_on_submit():
        usn = form.usn.data.strip()
        student = Student.query.filter_by(usn=usn).first()
        if student:
            session.clear()
            session['role'] = 'student'
            session['student_id'] = student.id
            session['student_name'] = student.name
            flash(f'Logged in as {student.name}', 'success')
            return redirect(url_for('student.student_dashboard'))
        else:
            flash('USN not found. Ask admin to register you.', 'danger')
    return render_template('login_student.html', form=form)

# Staff login (Staff ID only)
@auth_bp.route('/login/staff', methods=['GET', 'POST'])
def login_staff():
    form = StaffLoginForm()
    if form.validate_on_submit():
        staff_id = form.staff_id.data.strip()
        staff = Staff.query.filter_by(staff_id=staff_id).first()
        if staff:
            session.clear()
            session['role'] = 'staff'
            session['staff_id'] = staff.id
            session['staff_name'] = staff.name
            flash(f'Logged in as {staff.name}', 'success')
            return redirect(url_for('staff.staff_dashboard'))
        else:
            flash('Staff ID not found. Ask admin to register you.', 'danger')
    return render_template('login_staff.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth.home'))