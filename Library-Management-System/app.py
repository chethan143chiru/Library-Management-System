import os
from flask import Flask
from config import Config
from extensions import db, migrate

def create_app():
    # Initialize Flask app
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure upload and instance directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.student_routes import student_bp
    from routes.staff_routes import staff_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(staff_bp, url_prefix='/staff')

    # Optional: home route for root
    @app.route('/')
    def home():
        return "<h2>Welcome to Library Management System</h2><p>Please login as Admin / Staff / Student</p>"

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    # Run Flask development server
    app.run(debug=True)