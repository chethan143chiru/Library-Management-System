from flask import Blueprint, render_template, session, redirect, url_for, flash, current_app, send_from_directory
from helpers import login_required
from models import Book, IssuedBook, Student
from extensions import db

student_bp = Blueprint('student', __name__, template_folder='../templates')

@student_bp.route('/dashboard')
@login_required('student')
def student_dashboard():
    student_id = session.get('student_id')
    books = Book.query.all()
    student = Student.query.get(student_id)
    issued = IssuedBook.query.filter_by(student_id=student_id).order_by(IssuedBook.issue_date.desc()).all()
    return render_template('student_dashboard.html', student=student, books=books, issued=issued)

@student_bp.route('/books')
@login_required('student')
def view_books():
    books = Book.query.all()
    return render_template('view_books.html', books=books)

@student_bp.route('/downloads/<filename>')
@login_required('student')
def download(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@student_bp.route('/read/<int:book_id>')
@login_required('student')
def read_online(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.ebook_filename:
        flash('No ebook available for this title', 'warning')
        return redirect(url_for('student.student_dashboard'))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], book.ebook_filename)