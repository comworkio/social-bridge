import tweepy
import os

from utils.common import is_null_env

def is_twitter_enabled():
    return not any(is_null_env(p) for p in ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET', 'TWITTER_BEARER_TOKEN'])

_TWITTER_CLIENT = None
if is_twitter_enabled():
    _TWITTER_CLIENT = tweepy.Client(
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN'), 
        access_token = os.getenv('TWITTER_ACCESS_TOKEN'), 
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    )
