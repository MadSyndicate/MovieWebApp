from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

    def __str__(self):
        return str(self.username)

    def __repr__(self):
        return str(self.username)

class Movie(db.Model):

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    director = db.Column(db.String(80), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(250), nullable=False)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)