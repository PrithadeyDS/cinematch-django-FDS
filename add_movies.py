import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinematch.settings')
django.setup()

from movies.models import Movie


movies = [
    ["Interstellar", "Sci-Fi", "Emotional", 2014, 4.8,
     "Explorers travel through space searching for a new home for humanity."],

    ["Knives Out", "Mystery", "Thrilling", 2019, 4.6,
     "A detective investigates a mysterious family case."],

    ["The Intern", "Comedy", "Cozy", 2015, 4.5,
     "A retired professional begins a new journey as an intern."],

    ["Inside Out", "Animation", "Emotional", 2015, 4.7,
     "A story about emotions, growing up and change."],

    ["La La Land", "Musical", "Romantic", 2016, 4.5,
     "Two ambitious artists pursue their dreams."],

    ["The Martian", "Sci-Fi", "Inspiring", 2015, 4.6,
     "An astronaut uses science and determination to survive."],

    ["Enola Holmes", "Mystery", "Fun", 2020, 4.2,
     "A young detective sets out to solve a mystery."],

    ["Paddington", "Comedy", "Cozy", 2014, 4.6,
     "A friendly bear begins a new life in London."],
]


for movie in movies:
    Movie.objects.get_or_create(
        title=movie[0],
        defaults={
            "genre": movie[1],
            "mood": movie[2],
            "release_year": movie[3],
            "rating": movie[4],
            "description": movie[5],
        }
    )


print("Movies added successfully!")