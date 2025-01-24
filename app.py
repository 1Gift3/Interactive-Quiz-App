from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# First we will intialize the Flask App
app = Flask(__name__)

# We then  here confirgure our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
#This here will be used for our session management the Secret Key
app.config['SECRET_KEY'] = 'your_secret_key' 


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# Lets inittialize placeholder extensions e.g  SQLAlchemy

#Firstly we have to define our route
@app.route('/')
def home():
    return "Welcomed are you, to the Alx Portfolio Quiz App!"

#Lets now run the Application
if __name__ == '__main__':
    app.run(debug=True)

    