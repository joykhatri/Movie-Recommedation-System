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
        fields = "__all__"

class PopularContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = "__all__"

class UpcomingContentSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = UpcomingContent
        fields = "__all__"