from flask import Blueprint, request, jsonify
from app import db
from models import Quiz, Question, QuizResult

main = Blueprint('main', __name__)

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
