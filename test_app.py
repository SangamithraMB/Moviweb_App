import pytest
from app import app, db, data_manager
from datamanager.models import User, Movie


@pytest.fixture
def client():
    """Sets up a test client for the Flask app and initializes the database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for the test database
            yield client  # Provide the client for tests
        db.drop_all()  # Drop tables after tests are done


# Test routes
def test_home_route(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App" in response.data


def test_list_users_route(client):
    """Test the /users route, which lists all users."""
    # Add a test user to the database
    user = User(name="John Doe")
    db.session.add(user)
    db.session.commit()

    # Test the /users route
    response = client.get('/users')
    assert response.status_code == 200
    assert b"John Doe" in response.data


def test_add_user(client):
    """Test adding a user via the /add_user route."""
    response = client.post('/add_user', data=dict(name="Jane Doe"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Jane Doe" in response.data


def test_user_movies_route(client):
    """Test the /users/<user_id> route to display a user's movies."""
    # Add a test user and movie
    user = User(name="Alice")
    movie = Movie(name="Inception", director="Christopher Nolan", year=2010, rating=9.0, user_id=user.id)
    db.session.add(user)
    db.session.add(movie)
    db.session.commit()

    # Test the /users/<user_id> route
    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert b"Inception" in response.data


def test_add_movie(client):
    """Test adding a movie to a user."""
    # Add a test user
    user = User(name="Bob")
    db.session.add(user)
    db.session.commit()

    # Test the /users/<user_id>/add_movie route
    response = client.post(f'/users/{user.id}/add_movie', data=dict(
        name="The Matrix", director="Wachowskis", year=1999, rating=8.7
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"The Matrix" in response.data


# Test DataManager
def test_data_manager_get_all_users(client):
    """Test DataManager's get_all_users method."""
    user = User(name="Charlie")
    db.session.add(user)
    db.session.commit()

    users = data_manager.get_all_users()
    assert len(users) == 1
    assert users[0].name == "Charlie"


def test_data_manager_add_user(client):
    """Test DataManager's add_user method."""
    new_user = User(name="David")
    data_manager.add_user(new_user)

    users = data_manager.get_all_users()
    assert len(users) == 1
    assert users[0].name == "David"


def test_data_manager_add_movie(client):
    """Test DataManager's add_movie method."""
    user = User(name="Eve")
    db.session.add(user)
    db.session.commit()

    new_movie = Movie(name="Interstellar", director="Christopher Nolan", year=2014, rating=8.6, user_id=user.id)
    data_manager.add_movie(new_movie)

    movies = data_manager.get_user_movies(user.id)
    assert len(movies) == 1
    assert movies[0].name == "Interstellar"
