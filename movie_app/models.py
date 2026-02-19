from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)

    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    tagline = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_average= models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title