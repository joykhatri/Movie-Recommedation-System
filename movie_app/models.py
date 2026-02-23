from django.db import models

class Actor(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=500, null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    known_for_department = models.CharField(max_length=100, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)

    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=[
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
    ])
    overview = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    tagline = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_average= models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    cast = models.ManyToManyField(Actor, related_name="movies", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class TrendingContent(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=10, choices=[
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
    ])
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    tagline = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    cast = models.ManyToManyField(Actor, related_name="trending_content", blank=True)
    trending = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-popularity']


class UpcomingContent(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=[
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
    ])
    overview = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    tagline = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    cast = models.ManyToManyField(Actor, related_name="upcoming_content", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['release_date']

    def __str__(self):
        return self.title