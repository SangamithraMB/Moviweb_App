# Moviweb_App

MovieWeb App is a Flask-based web application that allows users to add, view, update, and delete movies for each registered user. The application integrates with the OMDb API to retrieve additional movie details when adding new movies and provides a clean, responsive UI using Bootstrap.

## Features

- **User Management**: Add, view, and delete users.
- **Movie Management**: Add, view, update, and delete movies associated with each user.
- **OMDb API Integration**: Fetch movie details automatically when a movie is added.
- **Responsive Design**: Designed with Bootstrap for a mobile-friendly experience.
  
## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite
- **API Integration**: OMDb API

## Prerequisites

- Python 3.x
- Flask and other dependencies from `requirements.txt`
- OMDb API key (stored in a `.env` file)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SangamithraMB/Moviweb_App.git
   cd Moviweb_App
   
2. Install Dependencies:
Use pip to install the required Python packages:
   ```bash
   pip install -r requirements.txt

3. Set Up .env File:
Create a .env file in the root directory and add your OMDb API key:
   OMDB_API_KEY=your_api_key_here

4. Run the Application:
   ```bash
   python app.py
   
5. 	Access the App:
	• Visit http://127.0.0.1:5000 in your browser.

## Testing

Run test_app.py to test application functionalities:
   ```bash
   python test_app.py
   ```

## .gitignore

Important files and folders are excluded in .gitignore:
```
    .env
    __pycache__/
    *.pyc
   
```

## Environment Variables
| Variable       | Description                                    |
|----------------|------------------------------------------------|
| `OMDB_API_KEY` | Your OMDb API key for fetching movie details   |


## Project Structure

```
Moviweb_App/
│
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
├── .gitignore            # Files to ignore in version control
├── .env                  # Environment variables
├── test_app.py           # Unit tests for the application
├── README.md             # Project documentation
│
├── datamanager/
│   ├── __init__.py               # Initializes data manager package
│   ├── data_manager_interface.py # Interface for data management
│   ├── models.py                 # Database models
│   └── sqlite_data_manager.py    # SQLite implementation
│
├── data/                         # Database file storage
│
├── static/                       # Static files for styling
│   ├── css/
│   └── bootstrap/
│
└── templates/                    # HTML templates for rendering pages
```

### Usage

	•	Add User: Navigate to “Add User” to create a new user.
	•	View Users: See all registered users and view their associated movies.
	•	Manage Movies: For each user, you can add, update, or delete movies.
	•	OMDb Integration: When adding a new movie, details will be fetched from the OMDb API if available.

### API Documentation

This app interacts with the OMDb API to fetch movie details. For more details on available endpoints and usage, see the OMDb API Documentation.


### Contributing

Contributions are welcome! Please submit a pull request or create an issue to start a discussion.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgements
```
	•	Flask
	•	OMDb API
	•	Bootstrap
```

