from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'trending', TrendingContentView, basename="trending")
router.register(r'actor', ActorView, basename="actor")
router.register(r'popular_content', PopularContentView, basename="popular_content")
router.register(r'upcoming_content', UpcomingContentView, basename="upcoming_content")
router.register(r'top_rated_content', TopRatedContentView, basename="top_rated_content")
router.register(r'tv_show_season', TVShowSeasonView, basename="tv_show_season")
router.register(r'season_episodes', SeasonEpisodeView, basename="season_episodes")
urlpatterns = router.urls