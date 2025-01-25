from flask_sqlalchemy import SQLAlchemy 

# Lets Initialize our SQLAlchemy 
db = SQLAlchemy()

# On now to the user model
class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Corrected case
    password = db.Column(db.String(150), nullable=False)

# Our Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)


# Questions Model 
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    choices = db.Column(db.PickleType, nullable=False)  
    answer = db.Column(db.String(200), nullable=False)

# Then our Quiz Results Model
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
             
