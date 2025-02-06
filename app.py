import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


# Initialize the Flask app
app = Flask(__name__)

# Configure app settings
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz_app.db'  # Database URI
app.config['SECRET_KEY'] = 'your_secret_key'  # Session management secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    choices = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(255), nullable=False)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()    

# Home page (renders HTML template)
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

#user dash board
@app.route('/dashboard')
@login_required
def dashboard():
    results = QuizResult.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", results=results)



# Route to display a quiz
@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0

    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and user_answer == question.answer:
            score += 1

    # Saving the quiz result in the database
    result = QuizResult(user_id=current_user.id, quiz_id=quiz_id, score=score)
    db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Quiz submitted!", "score": score, "total": len(questions)})


# Route to verify user login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirects to the dashboard after login

        return jsonify({"message": "Invalid username or password"}), 401

    return render_template("login.html")

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        existing_user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.commit()
        return jsonify({"message": "User password updated"}), 200
    else:
        new_user = User(username=username, password=bcrypt.generate_password_hash(password).decode("utf-8"))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "New user added"}), 201

# Route to add a new quiz
@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'message': 'Title is required'}), 400
    
    # Create a new quiz
    new_quiz = Quiz(title=title, description=description)
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz has been added'}), 201

 @app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
   

# Run the Flask application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
