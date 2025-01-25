from app import app, db
from models import User, Quiz, Question, QuizResult

# Create test data
with app.app_context():
    # Adds a test user
    user = User(username='test_user', password='password123')
    db.session.add(user)

    # Adding  test quiz
    quiz = Quiz(title='Python Basics')
    db.session.add(quiz)
    db.session.commit()  # Commit so we can reference the quiz ID

    # Add questions for all the quiz
    question1 = Question(
        quiz_id=quiz.id,
        question="What is the output of print(2 + 3)?",
        choices=["5", "23", "Error", "None of the above"],
        answer="5"
    )
    question2 = Question(
        quiz_id=quiz.id,
        question="Which keyword is used to define a function in Python?",
        choices=["function", "def", "define", "lambda"],
        answer="def"
    )
    db.session.add_all([question1, question2])

    # Adding a test result
    result = QuizResult(user_id=user.id, quiz_id=quiz.id, score=2)
    db.session.add(result)

    # Commiting all changes
    db.session.commit()

print("Test data added!")
