from rest_framework.generics import ListAPIView
from movie_app.models import TrendingContent
from movie_app.serializers import TrendingContentSerializer

class TrendingContentView(ListAPIView):
    serializer_class = TrendingContentSerializer

    def get_queryset(self):
        return TrendingContent.objects.filter(trending=True).order_by('-popularity')