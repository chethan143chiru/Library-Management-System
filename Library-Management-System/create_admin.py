from getpass import getpass
from app import create_app
from extensions import db
from models import Admin

app = create_app()

with app.app_context():
    username = input("Enter admin username: ")
    name = input("Enter admin name: ")
    password = getpass("Enter admin password: ")

    # Check if username already exists
    if Admin.query.filter_by(username=username).first():
        print("❌ Admin with that username already exists.")
    else:
        admin = Admin(username=username, name=name)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created successfully!")