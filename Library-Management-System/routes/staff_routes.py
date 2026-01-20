import os
from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app, send_from_directory, request
from helpers import login_required
from forms import AddBookForm, IssueBookForm
from models import Book, Student, IssuedBook
from extensions import db
from werkzeug.utils import secure_filename
from datetime import datetime

staff_bp = Blueprint('staff', __name__, template_folder='../templates')

# Allowed file extensions helper
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return '.' in filename and ext in current_app.config['ALLOWED_EXTENSIONS']

# Staff dashboard: view books + issued books
@staff_bp.route('/dashboard')
@login_required('staff')
def staff_dashboard():
    books = Book.query.all()
    issued = IssuedBook.query.order_by(IssuedBook.issue_date.desc()).all()
    return render_template('staff_dashboard.html', books=books, issued=issued)

# Add new book
@staff_bp.route('/books/add', methods=['GET', 'POST'])
@login_required('staff')
def add_book_staff():
    form = AddBookForm()
    if form.validate_on_submit():
        filename = None
        if form.ebook.data and allowed_file(form.ebook.data.filename):
            filename = secure_filename(form.ebook.data.filename)
            form.ebook.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        book = Book(
            title=form.title.data.strip(),
            author=form.author.data.strip(),
            publisher=form.publisher.data.strip(),
            year=form.year.data,
            category=form.category.data.strip(),
            copies=form.copies.data,
            ebook_filename=filename
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added', 'success')
        return redirect(url_for('staff.staff_dashboard'))
    return render_template('add_book.html', form=form)

@staff_bp.route('/books/<int:book_id>')
@login_required('staff')
def view_book_staff(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('view_book_staff.html', book=book)

# Delete a book
@staff_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required('staff')
def delete_book_staff(book_id):
    book = Book.query.get_or_404(book_id)
    # Remove ebook file if exists
    if book.ebook_filename:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], book.ebook_filename))
        except Exception:
            pass
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'success')
    return redirect(url_for('staff.staff_dashboard'))

# Issue book to student
@staff_bp.route('/issue', methods=['GET', 'POST'])
@login_required('staff')
def issue_book():
    form = IssueBookForm()
    if form.validate_on_submit():
        usn = form.usn.data.strip()
        student = Student.query.filter_by(usn=usn).first()
        if not student:
            flash('Student not found. Ask admin to register the student.', 'danger')
            return redirect(url_for('staff.issue_book'))

        book = Book.query.get(form.book_id.data)
        if not book:
            flash('Book ID not found', 'danger')
            return redirect(url_for('staff.issue_book'))

        if book.copies <= 0:
            flash('No copies available', 'warning')
            return redirect(url_for('staff.issue_book'))

        # Prevent issuing same book multiple times without return
        existing_issue = IssuedBook.query.filter_by(
            student_id=student.id,
            book_id=book.id,
            return_date=None
        ).first()
        if existing_issue:
            flash('This book is already issued to the student and not returned yet.', 'warning')
            return redirect(url_for('staff.issue_book'))

        issued = IssuedBook(
            book_id=book.id,
            student_id=student.id,
            issue_date=form.issue_date.data,
            due_date=form.due_date.data
        )
        book.copies -= 1
        db.session.add(issued)
        db.session.commit()
        flash('Book issued', 'success')
        return redirect(url_for('staff.staff_dashboard'))

    return render_template('issue_book.html', form=form)

# Download ebook safely
@staff_bp.route('/uploads/<filename>')
@login_required('staff')
def uploads(filename):
    book = Book.query.filter_by(ebook_filename=filename).first()
    if not book:
        flash("Unauthorized file access", "danger")
        return redirect(url_for('staff.staff_dashboard'))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)