from apscheduler.schedulers.background import BackgroundScheduler
from movie_app.services.import_movies import *

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(fetch_trending, 'interval', seconds=10)
    # scheduler.add_job(fetch_popular_actors, 'interval', minutes=1)
    scheduler.start()
    print("fetching movies")


# NOTE: you can't to run more than one scheduler at a time
# if one scheduler is running then comment out the other scheduler
# because TMDB has limited api calling (40 Requests / min), so it will fail after 40 requests
