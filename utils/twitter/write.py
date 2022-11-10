import os
import tweepy
from utils.common import sn_message
from utils.logger import quiet_log_msg

from utils.twitter.common import is_twitter_enabled

_api = None
if is_twitter_enabled():
    _api = tweepy.Client(
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN'), 
        access_token = os.getenv('TWITTER_ACCESS_TOKEN'), 
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    )

def tweet(username, message):
    if is_twitter_enabled() and None != _api:
        quiet_log_msg("DEBUG", "[twitter][tweet] Send message from {} : {}".format(username, message))
        _api.create_tweet(text = sn_message(username, message))
