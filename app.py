import os
from dotenv import load_dotenv
import sqlalchemy
from flask import Flask, request, jsonify
from data_manager import DataManager
from models import db, Movie
import fetch_movie_data as fmd

load_dotenv()
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

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_user_movies(user_id):
    movies = data_manager.get_movies(user_id)
    print(len(movies))
    return str(movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    data = request.form or request.json
    new_movie_name = data.get("movie_name", None)
    if new_movie_name:
        movie_data = fmd.fetch_movie_data(new_movie_name)
        print(movie_data)
        if movie_data["Response"] == 'True':
            fetched_name = movie_data.get("Title", None)
            fetched_release_year = movie_data.get("Year", None)
            fetch_director = movie_data.get("Director", None)
            fetched_post_url = movie_data.get("Poster", None)

            new_movie = Movie(
                user_id = user_id,
                name=fetched_name,
                director=fetch_director,
                release_year=fetched_release_year,
                poster_url=fetched_post_url
            )
            try:

                data_manager.add_movie(new_movie)
                return "Movie Added!", 200
            except sqlalchemy.exc.IntegrityError:
                return "Movie already exists in user collection!", 400

        return "No movie data found!", 400
    return "No Movie name provided!", 400

if __name__ == '__main__':
    """
        with app.app_context():
            db.create_all()
    """

    app.run(host="0.0.0.0", port=5002, debug=True)
