import pytest
from app import app , db, User, Quiz, Question, QuizResult


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

# Create test data
    with app.app_context():
    # Adds a test user
        db.create_all()
        create_test_data()

    yield client

    with app.app_context():
        db.drop_all()   

def create_test_data():
    #We adding a test user
    user = User(username='first_user', password='password123') 
    db.session.add(user)        

    # Adding  test quiz
    quiz = Quiz(title='Python Basics', description= 'A basic quiz on python')
    db.session.add(quiz)
    db.session.commit()  # Commit so we can reference the quiz id

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

def test_add_user(client):
    response = client.post('/add_user', json={
        'username': 'unique_user',
        'password': 'testpass'
    })
    print("Response JSON:", response.json)
    assert response.status_code == 201
    assert response.json['message'] == 'New user added'

def test_login(client):
    client.post ('/add_user', json={
        'username': 'unique_user_for_login',
        'password': 'testpass'
    })    
    response = client.post('/login', json={
         'username': 'unique_user_for_login',
         'password': 'testpass'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'


print("Test data added!")
