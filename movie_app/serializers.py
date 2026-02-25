from rest_framework import serializers
from movie_app.models import *

class PopularActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "tmdb_id", "name", "profile_path", "popularity", "known_for_department"]

class TrendingContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = TrendingContent
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "trending", "cast", "videos", "updated_at"]

class PopularContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "cast", "videos", "updated_at"]

class UpcomingContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = UpcomingContent
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "poster_path", "backdrop_path", "cast", "videos", "created_at"]

class TopRatedContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "cast", "videos", "updated_at"]

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id", "season_number", "name", "overview", "air_date", "episode_count", "poster_path"]

class TVShowSeasonSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "cast", "videos", "seasons", "updated_at"]

class SeasonEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "episode_number", "name", "overview", "air_date", "still_path", "vote_average"]