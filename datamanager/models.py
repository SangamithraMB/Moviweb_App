from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)

    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return self.username


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.name} ({self.year})>'

    def __str__(self):
        return f"{self.name} - {self.year}, {self.director}, {self.rating}"