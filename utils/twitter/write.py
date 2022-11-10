import os
import tweepy
from utils.common import sn_message

from utils.twitter.common import is_twitter_enabled

_api = None
if is_twitter_enabled():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
    _api = tweepy.API(auth)

def tweet(username, message):
    if _api != None:
        _api.tweet(sn_message(username, message))
