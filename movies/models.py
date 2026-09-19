from django.db import models


class Movie(models.Model):

    title = models.CharField(max_length=100)

    genre = models.CharField(max_length=50)

    mood = models.CharField(max_length=50)

    release_year = models.IntegerField()

    rating = models.FloatField()

    description = models.TextField()

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.movie.title

# Create your models here.
