from apscheduler.schedulers.background import BackgroundScheduler
from movie_app.services.import_movies import *

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(fetch_trending_movies, 'interval', seconds=10)
    # scheduler.add_job(fetch_trending_tv, 'interval', seconds=10)
    # scheduler.add_job(fetch_popular_actors, 'interval', minutes=1)
    # scheduler.add_job(fetch_popular_content, 'interval', seconds=10)
    # scheduler.add_job(fetch_upcoming_content, 'interval', seconds=10)
    # scheduler.add_job(fetch_upcoming_hindi_content, 'interval', seconds=10)
    # scheduler.add_job(remove_released_content, 'interval', hours=24)
    scheduler.start()
    print("fetching movies")


# NOTE: you can't to run more than one scheduler at a time
# if one scheduler is running then comment out the other scheduler
# because TMDB has limited api calling (40 Requests / min), so it will fail after 40 requests

