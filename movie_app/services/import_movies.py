import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
from movie_app.models import TrendingContent, Actor, Movie, UpcomingContent, Season, Episode
import time
from datetime import datetime, date

BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY

session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))


def fetch_watch_providers(media_type, tmdb_id, title):
    watch_providers = []
    url = f"{BASE_URL}/{media_type}/{tmdb_id}/watch/providers"
    try:
        providers_response = session.get(url, params={"api_key": TMDB_API_KEY}, timeout=10)
        if providers_response.status_code == 200:
            provider_data = providers_response.json()
            results = provider_data.get("results", {})
            us_providers = results.get("US", {})
            for key in ["flatrate", "rent", "buy"]:
                if us_providers.get(key):
                    for p in us_providers[key]:
                        watch_providers.append({
                            "provider_id": p.get("provider_id"),
                            "provider_name": p.get("provider_name"),
                            "logo_path": p.get("logo_path")
                        })
        else:
            print(f"Failed to fetch providers for {title}")
    except requests.RequestException as e:
        print(f"Exception fetching providers for {title}: {e}")

    return watch_providers


def fetch_genres_and_tagline(media_type, content_id, title):
    genres = []
    tagline = ""
    detail_data = {}
    detail_url = f"{BASE_URL}/{media_type}/{content_id}"

    try:
        detail_response = session.get(
            detail_url,
            params={"api_key": TMDB_API_KEY, "append_to_response": "credits"},
            timeout=10
        )
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            genres = [g['name'] for g in detail_data.get("genres", [])]
            tagline = detail_data.get("tagline") or ""
        else:
            print(f"Failed to fetch details for {title}")
    except requests.RequestException as e:
        print(f"Exception fetching details for {title}: {e}")
    
    return genres, tagline, detail_data


def fetch_videos(media_type, tmdb_id, title):
    detail_url = f"{BASE_URL}/{media_type}/{tmdb_id}/videos"
    params = {"api_key": TMDB_API_KEY}

    try:
        detail_response = session.get(detail_url, params=params, timeout=10)
        detail_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching videos for {title}: {e}")
        
    results = detail_response.json().get("results", [])

    videos = [
        {
            "key": video["key"],
            "name": video["name"],
            "type": video["type"],
            "site": video["site"],
        }
        for video in results
        if video["site"] == "YouTube"
        and video["type"] in ["Teaser", "Trailer"]
        and video.get("official") is True
    ]
    return videos


def fetch_tv_season_details(tv_id):
    url = f"{BASE_URL}/tv/{tv_id}"
    params = {"api_key": TMDB_API_KEY}

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch TV details for {tv_id}: {e}")
        return {}

    return response.json()


def fetch_and_save_episodes(tv_id, season_obj):
    url = f"{BASE_URL}/tv/{tv_id}/season/{season_obj.season_number}"
    params = {"api_key": TMDB_API_KEY}

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch episode for season {season_obj.season_number}: {e}")
        return
    
    data = response.json()
    episodes = data.get("episodes", [])

    for ep in episodes:
        air_date = ep.get("air_date")
        if air_date:
            try:
                air_date = datetime.strptime(air_date, "%Y-%m-%d").date()
            except ValueError:
                air_date = None

        Episode.objects.update_or_create(
            season = season_obj,
            episode_number = ep.get("episode_number"),
            name = ep.get("name"),
            overview = ep.get("overview"),
            air_date = air_date,
            still_path = ep.get("still_path"),
            vote_average = ep.get("vote_average")
        )


def fetch_trending_content(media_type="tv"):
    if media_type == "movie":
        url = f"{BASE_URL}/trending/{media_type}/day"
    elif media_type == "tv":
        url = f"{BASE_URL}/trending/{media_type}/day"
    else:
        return
    
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits"
    }

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("TMDB API Error:", e)
        return
    
    contents = response.json().get("results", [])

    TrendingContent.objects.filter(media_type=media_type).update(trending=False)

    if not contents:
        print(f"No trending {media_type} found!")
        return

    for content in contents:
        tmdb_id = content.get("id")
        title = content.get("title") or content.get("name")
        release_date = content.get("release_date") or content.get("first_air_date")

        genres, tagline, detail_data = fetch_genres_and_tagline(media_type, tmdb_id, title)

        watch_providers = fetch_watch_providers(media_type, tmdb_id, title)

        videos = fetch_videos(media_type, tmdb_id, title)

        print(f"Saving movie: {title} ({tmdb_id}) with providers: {watch_providers}")

        try:
            trending_obj, _ = TrendingContent.objects.update_or_create(
                tmdb_id=tmdb_id,
                media_type=media_type,
                defaults={
                    "title": title,
                    "genres": genres,
                    "tagline": tagline,
                    "overview": detail_data.get("overview") or content.get("overview"),
                    "poster_path": detail_data.get("poster_path") or content.get("poster_path"),
                    "backdrop_path": detail_data.get("backdrop_path") or content.get("backdrop_path"),
                    "release_date": release_date,
                    "vote_average": detail_data.get("vote_average") or content.get("vote_average"),
                    "popularity": detail_data.get("popularity") or content.get("popularity"),
                    "watch_providers": watch_providers,
                    "videos": videos,
                    "trending": True,
                },
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")
            continue

        fetch_and_save_cast(tmdb_id, media_type, trending_obj)

        time.sleep(1.5)

    print(f"Trending {media_type} synced successfully")


def remove_not_trending_content():
    TrendingContent.objects.filter(trending=False).delete()
    print("Non-trending content removed successfully")


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


def fetch_popular_content(media_type="tv"):
    # url = f"{BASE_URL}/movie/popular"
    url = f"{BASE_URL}/tv/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "page": 1,
        "append_to_response": "credits"
    }

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch popular content: {e}")
        return

    contents_data = response.json()

    for content_data in contents_data.get("results", []):
        content_id = content_data.get("id")
        title = content_data.get("title") or content_data.get("name")
        release_date = content_data.get("release_date") or content_data.get("first_air_date") or None
        
        genres, tagline, detail_data = fetch_genres_and_tagline(media_type, content_id, title)
        watch_providers = fetch_watch_providers(media_type, content_id, title)
        videos = fetch_videos(media_type, content_id, title)

        print(f"Saving content: {title} with providers: {watch_providers}")

        try:
            content, _ = Movie.objects.update_or_create(
                tmdb_id=content_id,
                defaults={
                    "title": title,
                    "media_type": media_type,
                    "overview": detail_data.get("overview"),
                    "tagline": tagline,
                    "genres": genres,
                    "release_date": release_date,
                    "popularity": detail_data.get("popularity"),
                    "vote_average": detail_data.get("vote_average"),
                    "poster_path": detail_data.get("poster_path"),
                    "backdrop_path": detail_data.get("backdrop_path"),
                    "watch_providers": watch_providers,
                    "videos": videos
                },
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")

        fetch_and_save_cast(content_id, media_type, content)

        if media_type == "tv":
            try:
                tv_details = fetch_tv_season_details(content_id)
                seasons_data = tv_details.get("seasons", [])

                for season in seasons_data:
                    air_date = season.get("air_date")
                    if air_date:
                        try:
                            air_date = datetime.strptime(air_date, "%Y-%m-%d").date()
                        except ValueError:
                            air_date = None

                    season_obj, _ = Season.objects.update_or_create(
                        tv_show = content,
                        season_number = season.get("season_number"),
                        name = season.get("name"),
                        overview = season.get("overview"),
                        air_date = air_date,
                        episode_count = season.get("episode_count"),
                        poster_path = season.get("poster_path")
                    )
            except Exception as e:
                print(f"Error fetching season for {title}: {e}")
            
            fetch_and_save_episodes(content_id, season_obj)

        time.sleep(2)
    print("Popular Content synced successfully")


def fetch_upcoming_content(media_type="movie"):
    if media_type == "movie":
        url = f"{BASE_URL}/movie/upcoming"
    elif media_type == "tv":
        url = f"{BASE_URL}/tv/on_the_air"
    else:
        return

    params = {
        "api_key": TMDB_API_KEY,
        "page": 1,
        "append_to_response": "credits"
    }

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch upcoming content: {e}")
        return

    contents_data = response.json()

    for content_data in contents_data.get("results", []):
        content_id = content_data.get("id")
        title = content_data.get("title") or content_data.get("name")
        release_date = content_data.get("release_date") or content_data.get("first_air_date")

        try:
            release_date_obj = date.fromisoformat(release_date)
        except ValueError as e:
            continue

        if release_date_obj <= date.today():
            continue

        genres, tagline, detail_data = fetch_genres_and_tagline(media_type, content_id, title)
        watch_providers = fetch_watch_providers(media_type, content_id, title)
        videos = fetch_videos(media_type, content_id, title)

        print(f"Saving content: {title}")

        try:
             content, _ = UpcomingContent.objects.update_or_create(
                tmdb_id=content_id,
                defaults={
                    "title": title,
                    "media_type": media_type,
                    "overview": detail_data.get("overview"),
                    "genres": genres,
                    "tagline": tagline,
                    "release_date": release_date,
                    "popularity": detail_data.get("popularity"),
                    "poster_path": detail_data.get("poster_path"),
                    "backdrop_path": detail_data.get("backdrop_path"),
                    "watch_providers": watch_providers,
                    "videos": videos
                }
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")
        
        fetch_and_save_cast(content_id, media_type, content)
        time.sleep(2)
    print(f"Upcoming {media_type} synced successfully")


def fetch_upcoming_hindi_content(media_type="movie"):
    if media_type == "movie":
        url = f"{BASE_URL}/discover/movie"
        date_field = "primary_release_date.gte"
        sort_field = "primary_release_date.asc"
    else:
        url = f"{BASE_URL}/discover/tv"
        date_field = "first_air_date.gte"
        sort_field = "first_air_date.asc"

    params = {
        "api_key": TMDB_API_KEY,
        "with_original_language": "hi",
        "region": "IN",
        date_field: date.today().isoformat(),
        "sort_by": sort_field,
        "page": 3
    }

    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch upcoming content: {e}")
        return

    contents_data = response.json()

    for content_data in contents_data.get("results", []):
        content_id = content_data.get("id")
        title = content_data.get("title") or content_data.get("name")
        release_date = content_data.get("release_date") or content_data.get("first_air_date")

        try:
            release_date_obj = date.fromisoformat(release_date)
        except ValueError as e:
            continue

        if release_date_obj <= date.today():
            continue

        genres, tagline, detail_data = fetch_genres_and_tagline(media_type, content_id, title)
        watch_providers = fetch_watch_providers(media_type, content_id, title)
        videos = fetch_videos(media_type, content_id, title)

        print(f"Saving content: {title}")

        try:
             content, _ = UpcomingContent.objects.update_or_create(
                tmdb_id=content_id,
                defaults={
                    "title": title,
                    "media_type": media_type,
                    "overview": detail_data.get("overview"),
                    "genres": genres,
                    "tagline": tagline,
                    "release_date": release_date,
                    "popularity": detail_data.get("popularity"),
                    "poster_path": detail_data.get("poster_path"),
                    "backdrop_path": detail_data.get("backdrop_path"),
                    "watch_providers": watch_providers,
                    "videos": videos
                }
            )
        except Exception as e:
            print(f"Error saving {title}: {e}")
        
        fetch_and_save_cast(content_id, media_type, content)
        time.sleep(2)
    print(f"Upcoming {media_type} synced successfully")


def remove_released_content():
    UpcomingContent.objects.filter(
        release_date__lte=date.today()
    ).delete()
    print("Release Content removed successfully")
