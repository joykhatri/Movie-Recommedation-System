from rest_framework import serializers
from movie_app.models import TrendingContent

class TrendingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingContent
        fields = "__all__"