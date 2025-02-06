import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from extensions import db, bcrypt
from models import User, Quiz, Question, QuizResult

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Requirements for flash messages

# Configure app settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'  # Database URI
app.config['SECRET_KEY'] = 'your_secret_key'  # Session management secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Create database tables if they don't exist
with app.app_context():
    db.drop_all()
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirects to home after login
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('register'))  # Redirects to register if credentials are invalid

    return render_template('login.html')  # Renders the login template

@app.route('/')
def home():
    return render_template("index.html")

# Add other routes here...

# Run the Flask application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
