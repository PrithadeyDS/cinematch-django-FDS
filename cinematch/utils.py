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


def generate_release_trends_plot():
    import io
    import base64
    import matplotlib.pyplot as plt
    import pandas as pd

    # Get movie release years from the database
    movies = Movie.objects.values('release_year')

    # Convert database records into a DataFrame
    df = pd.DataFrame(list(movies))

    # Check whether release-year data exists
    if df.empty:
        return None

    # Remove missing release years
    df = df.dropna(subset=['release_year'])

    if df.empty:
        return None

    # Count movies released in each year
    year_counts = df['release_year'].value_counts().sort_index()

    # Create the line chart
    plt.figure(figsize=(10, 5))
    plt.plot(
        year_counts.index,
        year_counts.values,
        marker='o',
        linewidth=2
    )

    plt.title('Movie Release Trends Over the Years')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Convert chart into an image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode('utf-8')

    plt.close()

    return image_base64


def generate_top_genres_plot():

    # Fetch genre information from the movie database
    movies = Movie.objects.values('genre')

    # Convert database records into a DataFrame
    df = pd.DataFrame(list(movies))

    # Check whether data exists
    if df.empty:
        return None

    # Count movies belonging to each genre
    genre_counts = df['genre'].value_counts().head(5)

    # Create a horizontal bar chart
    plt.figure(figsize=(9, 5))

    genre_counts.sort_values().plot(
        kind='barh',
        color='mediumpurple'
    )

    plt.title('Top 5 Movie Genres')
    plt.xlabel('Number of Movies')
    plt.ylabel('Genre')
    plt.tight_layout()

    # Save the chart temporarily
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert chart into Base64 format
    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode('utf-8')

    plt.close()

    return image_base64


