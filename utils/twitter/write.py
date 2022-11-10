import os
import tweepy
from utils.common import sn_message
from utils.logger import log_msg, quiet_log_msg

from utils.twitter.common import is_twitter_enabled

_api = None
if is_twitter_enabled():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
    _api = tweepy.API(auth)

def tweet(username, message):
    if _api != None:
        quiet_log_msg("DEBUG", "[twitter][tweet] Send message from {} : {}".format(username, message))
        _api.tweet(sn_message(username, message))
