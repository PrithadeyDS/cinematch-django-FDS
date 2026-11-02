from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
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
    try:
        from cinematch.utils import generate_numerical_plot, generate_categorical_plot
        num_plot = generate_numerical_plot()
        cat_plot = generate_categorical_plot()
        charts_available = True
    except ImportError:
        num_plot = cat_plot = None
        charts_available = False

    context = {
        "num_plot": num_plot,
        "cat_plot": cat_plot,
        "charts_available": charts_available,
    }
    return render(request, "analytics.html", context)
