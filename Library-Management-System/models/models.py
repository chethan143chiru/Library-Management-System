from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ----------------- Admin Model -----------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120))

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify entered password against stored hash"""
        return check_password_hash(self.password_hash, password)


# ----------------- Student Model -----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(50), unique=True, nullable=False)  # Login ID
    name = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(255))  # stored photo filename


# ----------------- Staff Model -----------------
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)  # Login ID
    name = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(255))  # stored photo filename


# ----------------- Book Model -----------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))
    year = db.Column(db.Integer)
    category = db.Column(db.String(80))
    copies = db.Column(db.Integer, default=1)
    ebook_filename = db.Column(db.String(255))  # path of uploaded eBook


# ----------------- Issued Book Model -----------------
class IssuedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    issue_date = db.Column(db.Date, default=datetime.utcnow)  # auto-set
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date, nullable=True)  # null → not returned yet

    # Relationships (back-references)
    book = db.relationship("Book", backref=db.backref("issued_records", lazy=True))
    student = db.relationship("Student", backref=db.backref("issued_records", lazy=True))