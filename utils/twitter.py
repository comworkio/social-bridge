from ast import keyword
from TwitterSearch import *
from datetime import datetime
from utils.common import extract_alphanum, is_empty, is_true

import os
from utils.config import get_keywords, get_usernames
from utils.logger import log_msg, quiet_log_msg
from utils.redis import get_cache_value, set_cache_value

from utils.slack import slack_messages

ts = TwitterSearch (
    consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
    access_token = os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

def stream_keywoards(keyword, usernames):
    tso = TwitterSearchOrder() 
    tso.set_count(int(os.environ['TWITTER_MAX_RESULTS']))
    tso.set_keywords([keyword])
    
    try:
        for tweet in ts.search_tweets_iterable(tso):
            username = extract_alphanum(tweet['user']['name'])
            quiet_log_msg("DEBUG", "[twitter][stream_keywoards] found tweet with keyword = {}, from {}".format(keyword, username))
            cache_key = "{}#{}".format(username, tweet['id_str'])
            if username not in usernames or is_true(get_cache_value(cache_key)):
                continue
            timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').isoformat()
            content = "[{}] {}".format(timestamp, tweet['text'])
            quiet_log_msg("INFO", "[twitter][stream_keywoards] found tweet username = {}, content = {}".format(username, content))
            slack_messages(content, username, True)
            set_cache_value(cache_key, "true")
    except Exception as e:
        log_msg("ERROR", "[twitter][stream_keywoards] unexpected error : {}".format(e))

def stream_tweets():
    keywords = get_keywords()
    usernames = get_usernames()
    quiet_log_msg("INFO", "[twitter][stream_tweets] searching tweet from usernames = {}, keywords = {}".format(usernames, keywords))
    for keyword in keywords:
        stream_keywoards(keyword, usernames)
