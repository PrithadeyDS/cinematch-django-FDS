import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from movies.models import Movie


MOOD_RULES = (
    ({"Horror", "Thriller", "Mystery", "Crime"}, "Suspenseful"),
    ({"Action", "Adventure", "Science Fiction", "War"}, "Exciting"),
    ({"Romance"}, "Romantic"),
    ({"Drama", "History"}, "Emotional"),
    ({"Comedy", "Animation", "Family", "Music"}, "Happy"),
)


def mood_for(genres):
    genre_set = set(genres)
    for matching_genres, mood in MOOD_RULES:
        if genre_set & matching_genres:
            return mood
    return "Relaxing"


class Command(BaseCommand):
    help = "Import the bundled Kaggle 9000+ Movies dataset into SQLite."

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / "movies" / "data" / "9000plus.csv"
        if not csv_path.exists():
            raise CommandError(f"Dataset file not found: {csv_path}")

        existing = {}
        for movie in Movie.objects.all().iterator():
            existing.setdefault((movie.title.casefold(), movie.release_year), movie)

        seen = set()
        to_create = []
        to_update = []
        skipped = 0

        with csv_path.open(encoding="utf-8-sig", newline="") as dataset_file:
            reader = csv.DictReader(dataset_file)
            required = {"Release_Date", "Title", "Overview", "Vote_Average", "Genre"}
            if not required.issubset(reader.fieldnames or []):
                raise CommandError("Dataset is missing one or more required columns.")

            for row in reader:
                title = (row.get("Title") or "").strip()
                raw_genres = (row.get("Genre") or "").strip()
                release_date = (row.get("Release_Date") or "").strip()
                try:
                    year = int(release_date[:4])
                    rating = round(float(row.get("Vote_Average") or "") / 2, 1)
                except (ValueError, TypeError):
                    skipped += 1
                    continue

                genres = [genre.strip() for genre in raw_genres.split(",") if genre.strip()]
                if not title or not genres or not 1880 <= year <= 2035 or not 0 <= rating <= 5:
                    skipped += 1
                    continue

                key = (title.casefold(), year)
                if key in seen:
                    skipped += 1
                    continue
                seen.add(key)

                values = {
                    "genre": genres[0][:50],
                    "mood": mood_for(genres),
                    "description": (row.get("Overview") or "").strip() or "No plot summary provided.",
                    "rating": rating,
                }
                movie = existing.get(key)
                if movie is None:
                    to_create.append(Movie(title=title[:150], release_year=year, **values))
                else:
                    changed = False
                    for field, value in values.items():
                        if getattr(movie, field) != value:
                            setattr(movie, field, value)
                            changed = True
                    if changed:
                        to_update.append(movie)

        with transaction.atomic():
            Movie.objects.bulk_create(to_create, batch_size=500)
            if to_update:
                Movie.objects.bulk_update(
                    to_update,
                    ["genre", "mood", "description", "rating"],
                    batch_size=500,
                )

        self.stdout.write(self.style.SUCCESS(
            f"Kaggle import complete: {len(to_create)} added, "
            f"{len(to_update)} updated, {skipped} skipped; "
            f"{Movie.objects.count()} movies now in the database."
        ))
