from flask import Flask
from flask_migrate import Migrate
from models import db, User

# First we will intialize the Flask App
app = Flask(__name__)

# We then  here confirgure our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
#This here will be used for our session management the Secret Key
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Lets inittialize placeholder extensions e.g  SQLAlchemy

@app.route('/add-test-user')
def add_test_user():
    with app.app_context():
        # Checking for an existing user or add a new one
        existing_user = User.query.filter_by(username="test_user").first()
        if existing_user:
            existing_user.password = "new_password"  
            return "Updated existing user's password!"
        else:
            user = User(username="test_user", password="password123")
            db.session.add(user)
            db.session.commit()
            return "Added a new test user!"

#Firstly we have to define our route
@app.route('/')
def home():
    return "Welcomed are you, to the Alx Portfolio Quiz App!"

#Lets now run the Application
if __name__ == '__main__':
    app.run(debug=True)


    