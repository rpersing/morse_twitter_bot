import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    SECRET_ACCESS_TOKEN = os.environ["SECRET_ACCESS_TOKEN"]

    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created!")
    return api
