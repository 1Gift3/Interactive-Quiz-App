from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# User Model
class User(db.Model):
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
    
@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    new_quiz = Quiz(title=title)
    db.session.add(new_quiz)
    db.session.commit()

    return jsonify({'message': 'Quiz added successfully'}), 201

    
@app.route('/add_question', methods=['POST'])
def add_question():
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    question = data.get('question')
    choices = data.get('choices')
    answer = data.get('answer')

    if not all([quiz_id, question, choices, answer]):
        return jsonify({'message': 'All fields are required'}), 400

    new_question = Question(
        quiz_id=quiz_id,
        question=question,
        choices=choices,
        answer=answer
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question added successfully'}), 201

@app.route('/take_quiz/<int:quiz_id>', methods=['GET'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    questions_data = [
        {
            'id': q.id,
            'question': q.question,
            'choices': q.choices,
        }
        for q in questions
    ]

    return jsonify({
        'quiz_title': quiz.title,
        'questions': questions_data
    }), 200

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    user_id = data.get('user_id')
    quiz_id = data.get('quiz_id')
    score = data.get('score')

    if not all([user_id, quiz_id, score]):
        return jsonify({'message': 'All fields are required'}), 400

    new_result = QuizResult(user_id=user_id, quiz_id=quiz_id, score=score)
    db.session.add(new_result)
    db.session.commit()

    return jsonify({'message': 'Quiz results submitted successfully'}), 201

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    data = [
        {
            'id': quiz.id,
            'title': quiz.title,
            'questions': [
                {
                    'id': q.id,
                    'question': q.question,
                    'choices': q.choices,
                    'answer': q.answer  # Optional: exclude in a public API
                }
                for q in quiz.questions
            ]
        }
        for quiz in quizzes
    ]

    return jsonify(data), 200

# Quiz Model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # Relationship with Question
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"<Quiz {self.title}>"

# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    choices = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Question {self.question}>"

# QuizResult Model
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # Relationships to User and Quiz
    user = db.relationship('User', backref='quiz_results', lazy=True)
    quiz = db.relationship('Quiz', backref='quiz_results', lazy=True)

    def __repr__(self):
        return f"<QuizResult User: {self.user_id}, Quiz: {self.quiz_id}, Score: {self.score}>"
