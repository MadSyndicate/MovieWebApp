import os
import sqlalchemy
from flask import Flask, request, jsonify
from data_manager import DataManager
from models import db, User

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, 'data/database.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_users()
    print(users)
    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods=['POST'])
def create_user():

    data = request.form or request.json #TODO only for testing with postman, form only later
    print(data)
    new_user_name = data.get("username", None)
    if new_user_name:
        try:
            data_manager.create_user(new_user_name)
            return "New User Created!"
        except sqlalchemy.exc.IntegrityError:
            return "User already exists!", 400

    return "No username provided!", 400


if __name__ == '__main__':
    """
        with app.app_context():
            db.create_all()
    """

    app.run(host="0.0.0.0", port=5002, debug=True)
