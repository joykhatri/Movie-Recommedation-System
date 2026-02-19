from django.apps import AppConfig
import os

class MovieAppConfig(AppConfig):
    name = 'movie_app'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            from .scheduler import start
            start()