from rest_framework.viewsets import ModelViewSet
from movie_app.models import *
from movie_app.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class TrendingContentView(ModelViewSet):
    queryset = TrendingContent.objects.all()
    serializer_class = TrendingContentSerializer
    
    def list(self, request):
        trending = TrendingContent.objects.filter(trending=True).order_by('-popularity')

        media_type = request.query_params.get('media_type')
        if media_type in ['movie', 'tv']:
            trending = trending.filter(media_type=media_type)

        serializer = self.get_serializer(trending, many=True)
        return Response({
            "status": True,
            "message": "Trending Content are",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class ActorView(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = PopularActorSerializer

    def list(self, request):
        actor = Actor.objects.filter().order_by("-popularity")
        serializer = self.get_serializer(actor, many=True)
        return Response({
            "status": True,
            "message": "Popular Actors are",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class PopularContentView(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PopularContentSerializer

    def list(self, request):
        movie = Movie.objects.filter(popularity__gt=80).order_by('-popularity')

        media_type = request.query_params.get('media_type')
        if media_type in ['movie', 'tv']:
            movie = movie.filter(media_type=media_type)

        genres_params = request.query_params.get('genres')
        if genres_params:
            genres = [g.strip() for g in genres_params.split(',')]
            genre_filter = Q()
            for g in genres:
                genre_filter |= Q(genres__icontains=g)
                genre_filter |= Q(genres__contains=[{"name": g}])
            movie = movie.filter(genre_filter)

        serializer = self.get_serializer(movie, many=True)
        return Response({
            "status": True,
            "message": "Popular Movies are",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class UpcomingContentView(ModelViewSet):
    serializer_class = UpcomingContentSerializer

    def list(self, request):
        queryset = UpcomingContent.objects.all()

        media_type = request.query_params.get("media_type")
        if media_type in ["movie", "tv"]:
            queryset = queryset.filter(media_type=media_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Upcoming content fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class TopRatedContentView(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = TopRatedContentSerializer

    def list(self, request):
        movie = Movie.objects.filter(popularity__gt=80, vote_average__gt=8).order_by('-popularity')

        media_type = request.query_params.get('media_type')
        if media_type in ['movie', 'tv']:
            movie = movie.filter(media_type=media_type)

        serializer = self.get_serializer(movie, many=True)
        return Response({
            "status": True,
            "message": "Top Rated contents are",
            "data": serializer.data
        }, status=status.HTTP_200_OK)