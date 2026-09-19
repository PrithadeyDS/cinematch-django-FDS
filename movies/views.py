from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Watchlist


# HOME PAGE
def home(request):

    movies = Movie.objects.all()

    search = request.GET.get("search")
    mood = request.GET.get("mood")
    genre = request.GET.get("genre")

    # Search
    if search:
        movies = movies.filter(title__icontains=search)

    # Mood filter
    if mood:
        movies = movies.filter(mood__iexact=mood)

    # Genre filter
    if genre:
        movies = movies.filter(genre__iexact=genre)

    # Statistics
    total_movies = Movie.objects.count()

    total_genres = Movie.objects.values(
        "genre"
    ).distinct().count()

    watchlist_count = Watchlist.objects.count()

    return render(request, "home.html", {

        "movies": movies,

        "total_movies": total_movies,
        "total_genres": total_genres,
        "watchlist_count": watchlist_count,

        "search": search,
        "selected_mood": mood,
        "selected_genre": genre,

    })


# MOVIE DETAILS
def movie_detail(request, movie_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    return render(request, "movie_detail.html", {
        "movie": movie
    })


# ADD TO WATCHLIST
def add_to_watchlist(request, movie_id):

    if request.method == "POST":

        movie = get_object_or_404(
            Movie,
            id=movie_id
        )

        Watchlist.objects.get_or_create(
            movie=movie
        )

    return redirect("watchlist")


# WATCHLIST PAGE
def watchlist(request):

    items = Watchlist.objects.all()

    return render(request, "watchlist.html", {
        "items": items
    })


# REMOVE FROM WATCHLIST
def remove_from_watchlist(request, movie_id):

    if request.method == "POST":

        item = Watchlist.objects.filter(
            movie_id=movie_id
        ).first()

        if item:
            item.delete()

    return redirect("watchlist")