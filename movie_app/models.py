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
    watch_providers = models.JSONField(null=True, blank=True)
    videos = models.JSONField(null=True, blank=True)
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
    watch_providers = models.JSONField(null=True, blank=True)
    videos = models.JSONField(null=True, blank=True)
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
    watch_providers = models.JSONField(null=True, blank=True)
    videos = models.JSONField(null=True, blank=True)
    cast = models.ManyToManyField(Actor, related_name="upcoming_content", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['release_date']

    def __str__(self):
        return self.title


class Season(models.Model):
    tv_show = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.IntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    air_date = models.DateField(null=True, blank=True)
    episode_count = models.IntegerField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("tv_show", "season_number")
        ordering = ["season_number"]

    def __str__(self):
        return f"{self.tv_show.title} - Season{self.season_number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.IntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    air_date = models.DateField(null=True, blank=True)
    still_path = models.CharField(max_length=255, null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("season", "episode_number")
        ordering = ["episode_number"]

    def __str__(self):
        return f"{self.season.tv_show.title} - S{self.season.season_number}E{self.episode_number}"
    