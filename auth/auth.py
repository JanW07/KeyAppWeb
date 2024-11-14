from flask import Blueprint, render_template, request, redirect, url_for, session, current_app

auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Retrieve credentials from app config
        config = current_app.config['CREDENTIALS']
        valid_username = config.get('username')
        valid_password = config.get('password')

        if username == valid_username and password == valid_password:
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('auth.index'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')


# Logout route
@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))

# Root route (home page)
@auth_bp.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

# Decorator to protect routes
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
