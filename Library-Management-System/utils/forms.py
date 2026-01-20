from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, DateField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentLoginForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    submit = SubmitField('Login')

class StaffLoginForm(FlaskForm):
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    usn = StringField('USN', validators=[DataRequired(), Length(max=50)])
    photo = FileField('Photo (optional)')
    submit = SubmitField('Register')

class RegisterStaffForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    staff_id = StringField('Staff ID', validators=[DataRequired(), Length(max=50)])
    photo = FileField('Photo (optional)')
    submit = SubmitField('Register')

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[Optional(), Length(max=120)])
    publisher = StringField('Publisher', validators=[Optional(), Length(max=120)])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1000, max=9999)])
    category = StringField('Category', validators=[Optional(), Length(max=80)])
    copies = IntegerField('Copies', validators=[DataRequired(), NumberRange(min=1)])
    ebook = FileField('Ebook (pdf) (optional)')
    submit = SubmitField('Add Book')

class IssueBookForm(FlaskForm):
    usn = StringField('Student USN', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    issue_date = DateField('Issue Date', validators=[DataRequired()], format='%Y-%m-%d')
    due_date = DateField('Due Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Issue Book')