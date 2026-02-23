from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'trending', TrendingContentView, basename="trending")
router.register(r'actor', ActorView, basename="actor")
router.register(r'popular_content', PopularContentView, basename="popular_content")
router.register(r'upcoming_content', UpcomingContentView, basename="upcoming_content")
urlpatterns = router.urls