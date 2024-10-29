import os

from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.models import User, Movie
import requests


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db: SQLAlchemy):
        """Initialize the SQLiteDataManager with the SQLAlchemy instance."""
        self.db = db

    def get_all_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_user_movies(self, user_id):
        """Return a list of movies for a specific user."""
        user = User.query.get(user_id)
        return user.movies if user else []

    def add_user(self, user):
        """Add a new user to the database."""
        self.db.session.add(user)
        self.db.session.commit()

    def remove_user(self, user_id):
        """Remove a user from the database."""
        user = User.query.get(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def add_movie(self, user_id, movie):
        """Add a new movie to the database."""
        movie.user_id = user_id  # Set the user_id for the movie
        self.db.session.add(movie)
        self.db.session.commit()

    def update_movie(self, user_id, movie):
        """Update the details of a specific movie in the database."""
        existing_movie = Movie.query.get(movie.id)
        if existing_movie:
            existing_movie.name = movie.name
            existing_movie.director = movie.director
            existing_movie.year = movie.year
            existing_movie.rating = movie.rating
            existing_movie.user_id = user_id
            self.db.session.commit()

    def delete_movie(self, user_id, movie_id):
        """Delete a specific movie from the database."""
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()

    def get_movie_by_id(self, movie_id):
        """Get a movie by its ID."""
        return Movie.query.get(movie_id)

    def get_user_by_id(self, user_id):
        """Get a user by their ID."""
        return User.query.get(user_id)

    def get_user_by_username(self, username):
        """Return a user by username."""
        return User.query.filter_by(username=username).first()

    def fetch_movie_details(self, title):
        """Fetch movie details from OMDb API."""
        api_key = os.getenv('OMDB_API_KEY')  # Load the API key from environment variables
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
