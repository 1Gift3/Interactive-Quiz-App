from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from extensions import db, bcrypt
from flask_login import UserMixin

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password  # Will trigger the setter to hash the password

    @property
    def password(self):
        raise AttributeError("Your Password is not readable")

    @password.setter
    def password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifies a provided password against the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# Quiz Model
class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # Relationship with Question
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"<Quiz {self.title}>"

# Question Model
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    choices = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Question {self.question}>"

# QuizResult Model
class QuizResult(db.Model):
    __tablename__ = 'quiz_result'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # Relationships to User and Quiz
    user = db.relationship('User', backref='quiz_results', lazy=True)
    quiz = db.relationship('Quiz', backref='quiz_results', lazy=True)

    def __repr__(self):
        return f"<QuizResult User: {self.user_id}, Quiz: {self.quiz_id}, Score: {self.score}>"
