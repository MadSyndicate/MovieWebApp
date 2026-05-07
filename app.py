import os
from dotenv import load_dotenv
import sqlalchemy
from flask import Flask, request, render_template, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie
import fetch_movie_data as fmd

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(basedir, DATABASE_URL)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

@app.route('/')
def index():
    users = data_manager.get_users()
    for user in users:
        print(user.id, ':', user.username)
    return render_template('index.html', users=users, title="Home")


@app.route('/users', methods=['POST'])
def create_user():

    data = request.form or request.json #TODO only for testing with postman, form only later
    print(data)
    new_user_name = data.get("username", None)
    if new_user_name:
        try:
            data_manager.create_user(new_user_name)
            flash("User Created!", "success")
            return redirect(url_for('index'))
        except sqlalchemy.exc.IntegrityError:
            flash(f"User with name {new_user_name} already exists!", "error")
            return redirect(url_for('index'))

    flash(f"There was no username provided!", "error")
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_user_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    data = request.form or request.json
    new_movie_name = data.get("new_movie_name", None)
    new_movie_year = int(data.get("new_movie_year") or -1)
    if new_movie_name:
        movie_data = fmd.fetch_movie_data(new_movie_name)
        print(movie_data)
        if movie_data["Response"] == 'True':
            fetched_name = movie_data.get("Title", None)
            fetch_director = movie_data.get("Director", None)
            fetched_post_url = movie_data.get("Poster", None)
            if new_movie_year == -1:
                fetched_release_year = movie_data.get("Year", None)
            else:
                fetched_release_year = new_movie_year

            new_movie = Movie(
                user_id = user_id,
                name=fetched_name,
                director=fetch_director,
                release_year=fetched_release_year,
                poster_url=fetched_post_url
            )

            try:
                data_manager.add_movie(new_movie)
                flash("Movie Added!", "success")
                return redirect(url_for('list_user_movies', user_id=user_id))
            except sqlalchemy.exc.IntegrityError:
                flash(f"You allready have the movie '{new_movie_name}' in your collection!",
                      "error")
                return redirect(url_for('list_user_movies', user_id=user_id))

        flash(f"No movie data found for '{new_movie_name}'!",
              "error")
        return redirect(url_for('list_user_movies', user_id=user_id))

    flash(f"No movie name provided!",
          "error")
    return redirect(url_for('list_user_movies', user_id=user_id))



@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_user_movie(user_id,movie_id):
    data = request.form or request.json
    updated_movie_name = data.get("movie_name", None)
    if updated_movie_name:
        current_movie_data = data_manager.get_movie_by_ids(user_id, movie_id)
        if current_movie_data:
            current_movie_data.name = updated_movie_name
            try:
                data_manager.update_movie(current_movie_data)
                flash("Movie Updated!", "success")
                return redirect(url_for('list_user_movies', user_id=user_id))
            except sqlalchemy.exc.IntegrityError:
                flash(f"Movie '{updated_movie_name}' already exists in user collection!", "error")
                return redirect(
                    url_for('list_user_movies', user_id=user_id)
                )
        flash("Movie not found!", "danger")
        return redirect(url_for('list_user_movies', user_id=user_id))

    flash("No new movie name provided!", "error")
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id,movie_id):
    current_movie_data = data_manager.get_movie_by_ids(user_id, movie_id)
    if current_movie_data:
        try:
            data_manager.delete_movie(current_movie_data)
            flash("Movie Deleted!", "success")
            return redirect(url_for('list_user_movies', user_id=user_id))
        except sqlalchemy.exc.NoResultFound:
            flash("Movie not found!", "error")
            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            print(e)    # if unexpected thing happening
            flash("Something went wrong! Nothing was deleted", "error")
            return redirect(
                url_for('list_user_movies', user_id=user_id)
            )

    flash("Movie not found!", "error")
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    """
    with app.app_context():
        db.create_all()
    """

    app.run(host="0.0.0.0", port=5002, debug=True)
