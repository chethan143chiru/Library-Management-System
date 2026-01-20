import os
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app, send_from_directory
)
from models import Admin, Student, Staff, Book, IssuedBook
from extensions import db
from forms import RegisterStudentForm, RegisterStaffForm, AddBookForm, IssueBookForm
from helpers import login_required
from werkzeug.utils import secure_filename
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


# ----- Helpers -----
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', set())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


# ----- Admin Dashboard -----
@admin_bp.route('/dashboard')
@login_required('admin')
def admin_dashboard():
    students = Student.query.all()
    staff = Staff.query.all()
    books = Book.query.all()
    issued = IssuedBook.query.order_by(IssuedBook.issue_date.desc()).all()
    
    return render_template(
        'admin_dashboard.html',
        students=students,
        staff=staff,
        books=books,
        issued=issued
    )


# ----- Register Student -----
@admin_bp.route("/students/register", methods=["GET", "POST"])
@login_required('admin')
def register_student():
    form = RegisterStudentForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        usn = form.usn.data.strip()

        # check duplicate
        if Student.query.filter_by(usn=usn).first():
            flash('USN already registered', 'warning')
            return redirect(url_for('admin.register_student'))

        filename = None
        if form.photo.data and allowed_file(form.photo.data.filename):
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        new_student = Student(name=name, usn=usn, photo=filename)
        db.session.add(new_student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("register_student.html", form=form)


# ----- Register Staff -----
@admin_bp.route('/staff/register', methods=['GET', 'POST'])
@login_required('admin')
def register_staff():
    form = RegisterStaffForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        staff_id = form.staff_id.data.strip()

        if Staff.query.filter_by(staff_id=staff_id).first():
            flash('Staff ID already registered', 'warning')
            return redirect(url_for('admin.register_staff'))

        filename = None
        if form.photo.data and allowed_file(form.photo.data.filename):
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        staff = Staff(name=name, staff_id=staff_id, photo=filename)
        db.session.add(staff)
        db.session.commit()

        flash('Staff registered successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('register_staff.html', form=form)


# ----- Add Book -----
@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required('admin')
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        filename = None
        if form.ebook.data and allowed_file(form.ebook.data.filename):
            filename = secure_filename(form.ebook.data.filename)
            form.ebook.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        book = Book(
            title=form.title.data.strip(),
            author=form.author.data.strip() if form.author.data else None,
            publisher=form.publisher.data.strip() if form.publisher.data else None,
            year=form.year.data,
            category=form.category.data.strip() if form.category.data else None,
            copies=form.copies.data,
            ebook_filename=filename
        )
        db.session.add(book)
        db.session.commit()

        flash('Book added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_book.html', form=form)


# ----- View Book -----
@admin_bp.route('/books/<int:book_id>')
@login_required('admin')
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('view_book.html', book=book)


# ----- Delete Book -----
@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required('admin')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.ebook_filename:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], book.ebook_filename))
        except Exception:
            pass
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


# ----- Return Issued Book -----
@admin_bp.route('/issued/return/<int:issue_id>', methods=['POST'])
@login_required('admin')
def return_book(issue_id):
    issued = IssuedBook.query.get_or_404(issue_id)
    if issued.return_date:
        flash('Book already returned.', 'info')
    else:
        issued.return_date = datetime.utcnow().date()
        issued.book.copies = (issued.book.copies or 0) + 1
        db.session.commit()
        flash('Book returned successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


# ----- Download Ebook -----
@admin_bp.route('/uploads/<filename>')
@login_required('admin')
def uploads(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)