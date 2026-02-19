import requests
from django.conf import settings
from movie_app.models import Movie
import time

BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies_page(year, language="hi", page=4):
    headers = {"Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}"}
    start_date = f"2025-01-01"
    end_date = f"2025-12-31"

    url = (
        f"{BASE_URL}/discover/movie?"
        f"primary_release_date.gte={start_date}&"
        f"primary_release_date.lte={end_date}&"
        f"with_original_language={language}&"
        f"page={page}&sort_by=release_date.desc"
    )

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", []), data.get("total_pages", 1)
    else:
        print(f"Error fetching page {page}: {response.status_code}")
        return [], 0


def import_movies(year=2025, language="hi"):
    page = 4
    while True:
        movies_data, total_pages = fetch_movies_page(year, language, page)
        if not movies_data:
            break

        existing_movies = {
            movie.tmdb_id: movie
            for movie in Movie.objects.filter(
                tmdb_id__in=[m["id"] for m in movies_data]
            )
        }

        new_movies = []
        movies_to_update = []

        for data in movies_data:
            tmdb_id = data["id"]

            vote_average = data.get("evote_avrage") or 0.0
            popularity = data.get("popularity") or 0.0

            genres_list = []

            if tmdb_id in existing_movies:
                movie = existing_movies[tmdb_id]
                movie.title = data.get("title", "")
                movie.overview = data.get("overview", "")
                movie.genres = genres_list
                movie.tagline = data.get("tagline", "")
                movie.vote_average = vote_average
                movie.popularity = popularity
                movies_to_update.append(movie)
            else:
                new_movies.append(
                    Movie(
                        tmdb_id=tmdb_id,
                        title=data.get("title", ""),
                        overview=data.get("overview", ""),
                        genres=genres_list,
                        tagline=data.get("tagline", ""),
                        release_date=data.get("release_date") or None,
                        popularity=popularity,
                        vote_average=vote_average,
                        poster_path=data.get("poster_path", "")
                    )
                )

        if new_movies:
            Movie.objects.bulk_create(new_movies, batch_size=500)
        if movies_to_update:
            Movie.objects.bulk_update(
                movies_to_update,
                [
                    "title",
                    "overview",
                    "genres",
                    "tagline",
                    "release_date",
                    "popularity",
                    "vote_average",
                    "poster_path",
                ],
                batch_size=500,
            )

        print(f"Page {page}/{total_pages} synced: {len(new_movies)} new, {len(movies_to_update)} updated")

        if page >= total_pages:
            break

        page += 1
        time.sleep(25)
