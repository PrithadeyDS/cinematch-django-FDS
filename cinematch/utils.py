import base64
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from movies.models import Movie


def get_django_dataframe():
    movies = Movie.objects.all().values("title", "genre", "mood", "release_year", "rating")
    return pd.DataFrame(list(movies))


def generate_numerical_plot():
    df = get_django_dataframe()
    if df.empty:
        return None

    plt.figure(figsize=(7, 4))
    sns.set_theme(style="whitegrid")
    sns.histplot(df["rating"], bins=5, color="teal", kde=True)
    plt.title("Distribution of Movie Ratings", fontsize=11, fontweight="bold")
    plt.xlabel("Rating (out of 5.0)", fontsize=10)
    plt.ylabel("Number of Movies", fontsize=10)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    return image_base64


def generate_categorical_plot():
    df = get_django_dataframe()
    if df.empty:
        return None

    plt.figure(figsize=(7, 4))
    sns.set_theme(style="whitegrid")
    genre_counts = df["genre"].value_counts()
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis", orient="h")
    plt.title("Movie Count by Genre", fontsize=11, fontweight="bold")
    plt.xlabel("Number of Movies", fontsize=10)
    plt.ylabel("Genre", fontsize=10)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    return image_base64
