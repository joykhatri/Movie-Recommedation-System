from django.urls import path
from .views import TrendingContentView

urlpatterns = [
    path('trending/', TrendingContentView.as_view(), name="trending"),
]