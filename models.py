from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

# Lets Initialize our SQLAlchemy 
db = SQLAlchemy()
bcrypt = Bcrypt()

# On now to the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Corrected case
    password = db.Column(db.String(150), nullable=False)

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
             
