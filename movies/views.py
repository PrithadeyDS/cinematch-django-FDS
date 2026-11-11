from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Min, Max,Count

from cinematch.utils import generate_release_trends_plot 
from .models import Movie, Watchlist


GENRES = (
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western",
)
MOODS = (
    "Happy", "Emotional", "Exciting", "Relaxing", "Suspenseful", "Romantic",
    "Cozy", "Thrilling", "Fun", "Inspiring",
)


def home(request):
    movies = Movie.objects.all().order_by('-rating', 'title')
    search = request.GET.get("search")
    mood = request.GET.get("mood")
    genre = request.GET.get("genre")

    if search:
        movies = movies.filter(title__icontains=search)
    if mood:
        movies = movies.filter(mood__iexact=mood)
    if genre:
        movies = movies.filter(genre__iexact=genre)

    page_obj = Paginator(movies, 36).get_page(request.GET.get('page'))
    context = {
        "movies": page_obj.object_list,
        "page_obj": page_obj,
        "genres": GENRES,
        "moods": MOODS,
        "total_movies": Movie.objects.count(),
        "total_genres": Movie.objects.values("genre").distinct().count(),
        "watchlist_count": Watchlist.objects.count(),
        "search": search,
        "selected_mood": mood,
        "selected_genre": genre,
    }
    return render(request, "home.html", context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "movie_detail.html", {"movie": movie})


def add_to_watchlist(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id)
        Watchlist.objects.get_or_create(movie=movie)
    return redirect("watchlist")


def watchlist(request):
    items = Watchlist.objects.all()
    return render(request, "watchlist.html", {"items": items})


def remove_from_watchlist(request, movie_id):
    if request.method == "POST":
        item = Watchlist.objects.filter(movie_id=movie_id).first()
        if item:
            item.delete()
    return redirect("watchlist")



def analytics_view(request):

    # Generate existing charts
    try:
        from cinematch.utils import (
            generate_numerical_plot,
            generate_categorical_plot,
            generate_release_trends_plot,
            generate_top_genres_plot
        )

        num_plot = generate_numerical_plot()
        cat_plot = generate_categorical_plot()
        release_plot = generate_release_trends_plot()
        top_genres_plot = generate_top_genres_plot()

        charts_available = True

    except ImportError:
        num_plot = None
        cat_plot = None
        release_plot = None
        top_genres_plot = None
        charts_available = False

    # Calculate total number of movies
    total_movies = Movie.objects.count()

    # Calculate average rating
    average_rating = Movie.objects.aggregate(
        Avg('rating')
    )['rating__avg']

    # Count unique genres
    total_genres = Movie.objects.values(
        'genre'
    ).distinct().count()

    # Find earliest and latest release years
    release_years = Movie.objects.aggregate(
        Min('release_year'),
        Max('release_year')
    )

    earliest_year = release_years['release_year__min']
    latest_year = release_years['release_year__max']

      # INSIGHT 1: Find the genre containing the most movies
    top_genre = Movie.objects.values('genre').annotate(
        movie_count=Count('id')
    ).order_by('-movie_count').first()

    # INSIGHT 2: Find the movie with the highest rating
    highest_rated_movie = Movie.objects.order_by(
        '-rating'
    ).first()

    

    # Prepare data for HTML template
    context = {
        "num_plot": num_plot,
        "cat_plot": cat_plot,
        "release_plot": release_plot,
        "charts_available": charts_available,

        "total_movies": total_movies,
        "average_rating": round(average_rating, 2) if average_rating is not None else 0,
        "total_genres": total_genres,

        "earliest_year": earliest_year,
        "latest_year": latest_year,

        "top_genre_name": top_genre['genre'] if top_genre else "No data",
        "top_genre_count": top_genre['movie_count'] if top_genre else 0,
        "top_genres_plot": top_genres_plot,
        
        "top_movie_title": highest_rated_movie.title if highest_rated_movie else "No data",
        "top_movie_rating": highest_rated_movie.rating if highest_rated_movie else 0,
    }

    return render(request, "analytics.html", context)

    