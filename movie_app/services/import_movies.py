import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
from movie_app.models import TrendingContent, Actor
import time

BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY

# Create a session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# Fetch Trending Movies

def fetch_trending(media_type="movie"):
    url = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": TMDB_API_KEY}

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("TMDB API Error:", e)
        return

    movies = response.json().get("results", [])
    trending_ids = [movie["id"] for movie in movies]

    TrendingContent.objects.filter(media_type="movie").update(trending=False)

    if not movies:
        print("No trending movies found!")
        return

    for movie in movies:
        tmdb_id = movie.get("id")
        title = movie.get("title")
        release_date = movie.get("release_date") or None

        genres, tagline = [], ""
        detail_url = f"{BASE_URL}/movie/{tmdb_id}"
        try:
            detail_response = session.get(detail_url, params={"api_key": TMDB_API_KEY}, timeout=10)
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                genres = [g['name'] for g in detail_data.get("genres", [])]
                tagline = detail_data.get("tagline") or ""
            else:
                print(f"Failed to fetch details for {title} ({tmdb_id})")
        except requests.RequestException as e:
            print(f"Exception fetching details for {title} ({tmdb_id}): {e}")

        print(f"Saving movie: {title} ({tmdb_id})")  # debug

        try:
            trending_obj, _ = TrendingContent.objects.update_or_create(
                tmdb_id=tmdb_id,
                media_type="movie",
                defaults={
                    "title": title,
                    "genres": genres,
                    "tagline": tagline,
                    "overview": movie.get("overview"),
                    "poster_path": movie.get("poster_path"),
                    "backdrop_path": movie.get("backdrop_path"),
                    "release_date": release_date,
                    "vote_average": movie.get("vote_average"),
                    "popularity": movie.get("popularity"),
                    "trending": True
                }
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")

        fetch_and_save_cast(tmdb_id, media_type, trending_obj)

        time.sleep(1.5)


# Fetch Trending TV Shows

def fetch_trending(media_type="tv"):
    url = f"{BASE_URL}/trending/tv/day"
    params = {"api_key": TMDB_API_KEY}

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("TMDB API Error:", e)
        return

    shows = response.json().get("results", [])
    trending_ids = [show["id"] for show in shows]

    TrendingContent.objects.filter(media_type="tv").update(trending=False)

    if not shows:
        print("No trending TV shows found!")
        return

    for show in shows:
        tmdb_id = show.get("id")
        title = show.get("name")
        release_date = show.get("first_air_date") or None

        genres, tagline = [], ""
        detail_url = f"{BASE_URL}/tv/{tmdb_id}"
        try:
            detail_response = session.get(detail_url, params={"api_key": TMDB_API_KEY}, timeout=10)
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                genres = [g['name'] for g in detail_data.get("genres", [])]
                tagline = detail_data.get("tagline") or ""
            else:
                print(f"Failed to fetch details for {title} ({tmdb_id})")
        except requests.RequestException as e:
            print(f"Exception fetching details for {title} ({tmdb_id}): {e}")

        print(f"Saving TV show: {title} ({tmdb_id})")

        try:
            trending_obj, _ = TrendingContent.objects.update_or_create(
                tmdb_id=tmdb_id,
                media_type="tv",
                defaults={
                    "title": title,
                    "genres": genres,
                    "tagline": tagline,
                    "overview": show.get("overview"),
                    "poster_path": show.get("poster_path"),
                    "backdrop_path": show.get("backdrop_path"),
                    "release_date": release_date,
                    "vote_average": show.get("vote_average"),
                    "popularity": show.get("popularity"),
                    "trending": True
                }
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")
        fetch_and_save_cast(tmdb_id, media_type, trending_obj)
        time.sleep(1.5)

def fetch_and_save_cast(tmdb_id, media_type, obj):
    url = f"{BASE_URL}/movie/{tmdb_id}/credits"
    params = {"api_key": TMDB_API_KEY, "append_to_response": "credits"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        cast_list = response.json().get("cast", [])[:5]
    except requests.RequestException as e:
        print(f"Error fetching cast for {media_type} {tmdb_id}: {e}")
        return
    
    for actor_data in cast_list:
        actor_id = actor_data["id"]
        biography = None
        birthday = None
        
        try:
            person_url = f"{BASE_URL}/person/{actor_id}"
            person_response = session.get(
                person_url,
                params={"api_key": TMDB_API_KEY},
                timeout=10
            )
            person_response.raise_for_status()
            person_data = person_response.json()

            biography = person_data.get("biography")
            birthday = person_data.get("birthday")

        except requests.RequestException as e:
            print(f"Error fetching person {actor_id}: {e}")

        actor, _ = Actor.objects.update_or_create(
            tmdb_id=actor_data["id"],
            defaults={
                "name": actor_data["name"],
                "profile_path": actor_data.get("profile_path"),
                "popularity": actor_data.get("popularity"),
                "known_for_department": actor_data.get("known_for_department"),
                "biography": biography,
                "birthday": birthday,
            }
        )
        obj.cast.add(actor)

def fetch_popular_actors():
    url = f"{BASE_URL}/person/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "page": 5
    }

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching popular actors:", e)
        return
    
    actors = response.json().get("results", [])

    for person in actors:
        tmdb_id = person.get("id")
        name = person.get("name")

        actor, created = Actor.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "name": name,
                "profile_path": person.get("profile_path"),
                "popularity": person.get("popularity"),
            }
        )

        print(f"Saved popular actor: {name}")

        if not actor.biography:
            try:
                detail_url = f"{BASE_URL}/person/{tmdb_id}"
                detail_response = session.get(
                    detail_url,
                    params={"api_key": TMDB_API_KEY},
                    timeout=10
                )
                detail_response.raise_for_status()

                detail_data = detail_response.json()
                actor.biography = detail_data.get("biography")
                actor.birthday = detail_data.get("birthday")
                actor.save()

                print(f"Updated biography for {name}")
                time.sleep(1)
                
            except requests.RequestException as e:
                    print(f"Error fetching details for {name}: {e}")


        time.sleep(0.5)


