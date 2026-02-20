from apscheduler.schedulers.background import BackgroundScheduler
from movie_app.services.import_movies import *

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(fetch_trending, 'interval', seconds=10)
    # scheduler.add_job(fetch_popular_actors, 'interval', minutes=1)
    scheduler.start()
    print("fetching movies")


# NOTE: there are 2 fetch trending function in import_movies.py
# Both are for different purposes one for Movies and second is for TV Shows
# and i create both with same name, so you cannot run both function at same time 
# so you have to comment one function and then run the other function

# and you have to run one scheduler at a time
# if one scheduler is running then comment out the other scheduler
# because TMDB has limited api calling (40 Requests / min)