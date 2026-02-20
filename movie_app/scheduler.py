from apscheduler.schedulers.background import BackgroundScheduler
from movie_app.services.import_movies import *

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(fetch_trending, 'interval', seconds=10)
    # scheduler.add_job(fetch_popular_actors, 'interval', minutes=1)
    scheduler.start()
    print("fetching movies")