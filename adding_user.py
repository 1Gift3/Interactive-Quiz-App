from models import db, User
from app import app

with app.app_context():
    try:
        username = "new_user"
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print("This user already exists.")
        else:
            # Add a new one    
            new_user = User(username=username)
            new_user.password = "another_secure_password"
            db.session.add(new_user)
            db.session.commit()
            print(f"User {new_user.username} added very successfully !")
    except Exception as e:
        print(f"Ooops error occured: {e}")
        db.session.rollback()
    finally:
        db.session.close()

