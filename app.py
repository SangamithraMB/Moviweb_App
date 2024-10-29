import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.models import db, User, Movie

load_dotenv()

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "movie.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

data_manager = SQLiteDataManager(db)


@app.route('/')
def home():
    """
    Route for the home page.
    Returns a simple welcome message.
    """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
    Route to display the list of all users.
    Fetches the users from the data manager and renders the users.html template.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Route to display the movies for a specific user.
    Fetches the user's movies from the data manager and renders the user_movies.html template.

    Args:
        user_id (int): The ID of the user whose movies are to be displayed.
    """
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user_by_id(user_id)

    if user:
        return render_template('user_movies.html', user=user, movies=movies)
    else:
        return "User not found", 404


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route to add a new movie to a user's list of favorite movies.
    Displays a form for adding a movie on GET and handles form submission on POST.

    Args:
        user_id (int): The ID of the user who will own the movie.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        movie_title = request.form['movie_name']
        movie_details = data_manager.fetch_movie_details(movie_title)

        if movie_details and movie_details.get('Response') == 'True':
            director = movie_details.get('Director')
            year = movie_details.get('Year')
            rating = movie_details.get('imdbRating')

            new_movie = Movie(
                name=movie_title,
                director=director,
                year=year,
                rating=rating,
                user_id=user_id
            )
            data_manager.add_movie(user_id, new_movie)  # Add the movie to the database
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return "Movie not found.", 404

    return render_template('add_movie.html', user=user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user to the application.
    Displays a form for adding a user on GET and handles form submission on POST.
    """
    if request.method == 'POST':
        username = request.form['username']
        existing_user = data_manager.get_user_by_username(username)
        if existing_user:
            return "User already exists", 400

        new_user = User(username=username)
        data_manager.add_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route to update a specific movie's details.
    Displays a pre-filled form for updating movie details on GET and handles updates on POST.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be updated.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        movie.name = request.form['movie_name']
        movie.director = request.form['director']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        movie.user_id = user_id
        data_manager.update_movie(user_id, movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', movie=movie, user=user)  # Pass the user to the template


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Route to delete a specific movie from a user's list.
    Handles deletion upon POST request.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be deleted.
    """
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return "Movie not found", 404

    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_user', methods=['POST'])
def delete_user(user_id):
    """
    Route to delete a specific user from the system.
    Handles deletion upon POST request.

    Args:
        user_id (int): The ID of the user to be deleted.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    movies = data_manager.get_user_movies(user_id)

    for movie in movies:
        data_manager.delete_movie(user_id, movie.id)

    data_manager.remove_user(user_id)
    return redirect(url_for('list_users'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Custom error handler for 404 Not Found errors.
    Returns a custom 404 page.
    """
    return render_template('404.html', error=str(e)), 404


@app.errorhandler(500)
def internal_error(e):
    """
    Custom error handler for 500 Internal Server Error.
    Returns a custom 500 page.
    """
    return render_template('500.html', error=str(e)), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
