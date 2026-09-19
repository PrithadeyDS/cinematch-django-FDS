# CineMatch

CineMatch is a Django-based movie discovery and watchlist web application that helps users find movies based on their interests and mood.

The application supports movie search, mood-based discovery, genre filtering, detailed movie pages, and a database-backed watchlist.

## Features

- Search movies by title
- Filter movies by mood
- Filter movies by genre
- View detailed information about each movie
- Add movies to a watchlist
- Remove movies from the watchlist
- Dynamic movie, genre, and watchlist statistics
- Django Admin interface for managing movie data
- Responsive dark-themed interface
- Database operations using Django ORM
- CSRF-protected POST requests for watchlist operations

## Tech Stack

**Backend**
- Python
- Django

**Frontend**
- HTML
- CSS
- Django Template Language

**Database**
- SQLite

**Tools**
- VS Code
- Git
- GitHub

## How It Works

CineMatch follows Django's Model-Template-View architecture.

### Model

The models define the structure of the application's data.

The `Movie` model stores information such as:

- Title
- Genre
- Mood
- Release year
- Rating
- Description

The `Watchlist` model stores movies that have been saved for later.

### View

Django views contain the application's backend logic.

Views are responsible for:

- Retrieving movies from the database
- Searching movies
- Filtering movies by mood
- Filtering movies by genre
- Displaying movie details
- Adding movies to the watchlist
- Removing movies from the watchlist
- Calculating dashboard statistics

### Template

Django templates dynamically display data received from the views.

The main templates are:

- `home.html`
- `movie_detail.html`
- `watchlist.html`

## Django ORM

The project uses Django's Object-Relational Mapper to communicate with the SQLite database.

Examples of ORM operations used in CineMatch include:

```python
Movie.objects.all()
```

```python
Movie.objects.filter(title__icontains=search)
```

```python
Movie.objects.filter(mood__iexact=mood)
```

```python
Movie.objects.filter(genre__iexact=genre)
```

```python
Watchlist.objects.get_or_create(movie=movie)
```

This allows database operations to be performed using Python rather than writing SQL queries manually.

## GET and POST Requests

CineMatch uses GET requests for retrieving and filtering information.

Examples include:

- Searching
- Mood filtering
- Genre filtering

POST requests are used when the application modifies data, such as:

- Adding a movie to the watchlist
- Removing a movie from the watchlist

Django CSRF tokens are used to protect these POST requests.

## Project Structure

```text
cinematch/
│
├── manage.py
├── requirements.txt
├── add_movies.py
├── README.md
│
├── cinematch/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── movies/
    │
    ├── migrations/
    ├── static/
    │   └── css/
    │       └── style.css
    │
    ├── templates/
    │   ├── home.html
    │   ├── movie_detail.html
    │   └── watchlist.html
    │
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd cinematch
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Add the sample movie data

```bash
python add_movies.py
```

### 6. Start the Django development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Screenshots

### Home Page

Add a screenshot of the CineMatch home page here.

### Movie Details

Add a screenshot of a movie details page here.

### Watchlist

Add a screenshot of the CineMatch watchlist here.

## What I Learned

Building CineMatch helped me practice:

- Django project and application structure
- Django Models, Views and Templates
- URL routing
- Django ORM and QuerySets
- SQLite database integration
- GET and POST requests
- CSRF protection
- Search and filtering
- CRUD-style database operations
- Django Admin
- Static files and CSS
- Separating frontend and backend responsibilities

## Future Improvements

Possible future improvements include:

- User authentication
- Individual watchlists for different users
- Movie posters
- External movie API integration
- User ratings and reviews
- More advanced recommendation features

## Author

Built as a Django web development project.