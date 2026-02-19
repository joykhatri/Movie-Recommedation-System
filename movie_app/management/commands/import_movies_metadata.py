import pandas as pd
import ast
from movie_app.models import Movie

df = pd.read_csv('movies_metadata.csv', low_memory=False)
df.columns = df.columns.str.strip()
df.rename(columns={'id': 'tmdb_id'}, inplace=True)
df = df.drop_duplicates(subset='tmdb_id', keep='last')

for _, row in df.iterrows():
    try:
        tmdb_id = int(row['tmdb_id'])
    except (ValueError, TypeError):
        continue

    title = row.get('title')
    if not title or pd.isna(title):
        continue

    genres = None
    if pd.notnull(row.get('genres')):
        try:
            genres = ast.literal_eval(row['genres'])
        except (ValueError, SyntaxError):
            pass

    release_date = None
    if pd.notnull(row.get('release_date')):
        try:
            release_date = pd.to_datetime(row['release_date'], errors='coerce').date()
        except Exception:
            release_date = None

    movie, created = Movie.objects.update_or_create(
        tmdb_id=tmdb_id,
        defaults={
            'title': title,
            'overview': row.get('overview'),
            'genres': genres,
            'tagline': row.get('tagline'),
            'release_date': release_date,
            'popularity': row.get('popularity'),
            'vote_average': row.get('vote_average'),
            'poster_path': row.get('poster_path')
        }
    )

    if created:
        print(f"Created: {movie.title}")
    else:
        print(f"Updated: {movie.title}")
