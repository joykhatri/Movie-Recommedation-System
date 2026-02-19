from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from movie_app.services.import_movies import import_movies

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

def start():
    if not scheduler.running:
        import_movies()
        scheduler.add_job(
            import_movies,
            trigger="interval",
            # hours=12,
            minutes=1,
            id="sync_movies",
            replace_existing=True,
        )
        scheduler.start()
        print("Scheduler started: Movies sync every 12hr.")