from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(role=None):
    """
    Custom login_required decorator.
    - Redirects if user not logged in.
    - Restricts to role if specified.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'role' not in session:
                flash("Please log in to continue", "warning")
                return redirect(url_for('auth.home'))

            if role and session.get('role') != role:
                flash("You do not have permission to access this page", "danger")
                # send them to their own dashboard
                if session['role'] == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
                elif session['role'] == 'student':
                    return redirect(url_for('student.student_dashboard'))
                elif session['role'] == 'staff':
                    return redirect(url_for('staff.staff_dashboard'))
                else:
                    return redirect(url_for('auth.home'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper