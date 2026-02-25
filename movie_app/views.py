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
    

class TVShowSeasonView(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = TVShowSeasonSerializer

    def list(self, request):
        tvshows = Movie.objects.filter(media_type="tv").prefetch_related("seasons").order_by("-popularity")
        serializer = self.get_serializer(tvshows, many=True)
        return Response({
            "status": True,
            "message": "TV Shows seasons find successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk):
        tvshows = Movie.objects.filter(media_type="tv", pk=pk).prefetch_related("seasons").order_by("-popularity")
        if tvshows.exists():
            serializer = self.get_serializer(tvshows, many=True)
            return Response({
                "status": True,
                "message": "TV Shows seasons find successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "No TV Show found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
    

class SeasonEpisodeView(ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = SeasonEpisodeSerializer

    def list(self, request):
        tv_id = request.query_params.get("tv_id")
        season_number = request.query_params.get("season_number")

        if not tv_id or not season_number:
            return Response({
                "status": False,
                "message": "tv_id and season_number are required",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            season = Season.objects.get(tv_show__id=tv_id, season_number=int(season_number))
        except Season.DoesNotExist:
            return Response({
                "status": False,
                "message": "Season not found",
                "data": None
            }, status=404)
        
        episodes = Episode.objects.filter(season=season).order_by("episode_number")
        serializer = self.get_serializer(episodes, many=True)

        return Response({
            "status": True,
            "message": f"Episodes of season {season_number} fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    