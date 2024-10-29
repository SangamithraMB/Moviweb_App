from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Return a list of all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return a list of movies for a specific user."""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add a new user to the data source."""
        pass

    @abstractmethod
    def remove_user(self, user_id):
        """Remove a user from the data source."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        """Add a new movie to the data source."""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie):
        """Update the details of a specific movie in the data source."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Deletes a movie from the data source."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """Get a movie by its ID."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """Get a user by their ID."""
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        """Return a user by username."""
        pass

    @abstractmethod
    def fetch_movie_details(self, title):
        """Fetch movie details from OMDb API."""
        pass