from flask import Blueprint, request, session, redirect, url_for, flash
from functools import wraps  # Corrected import
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, url_for
from functools import wraps
# Create a Blueprint for auth
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Example login logic, adjust with your actual database check
        admin_username = "admin"  # Placeholder, fetch from config or database
        admin_password = "hashed_password"  # Placeholder, fetch and verify properly

        if username == admin_username and check_password_hash(admin_password, password):
            session['logged_in'] = True
            return redirect(url_for('auth.admin_console'))  # Ensure this is a valid endpoint
        else:
            flash('Invalid credentials')
    
    # Placeholder for actual login page rendering
    return "Login Page Placeholder"

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            # Correcting the endpoint name here
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function