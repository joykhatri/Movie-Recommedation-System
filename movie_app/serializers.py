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
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "trending", "cast", "updated_at"]

class PopularContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "cast", "updated_at"]

class UpcomingContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = UpcomingContent
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "poster_path", "backdrop_path", "cast", "created_at"]

class TopRatedContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "media_type", "title", "overview", "genres", "tagline", "release_date", "popularity", "vote_average", "poster_path", "backdrop_path", "cast", "updated_at"]
