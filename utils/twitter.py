import os
import requests
import re

from TwitterSearch import *
from datetime import datetime
from urlextract import URLExtract
from time import sleep

from utils.common import extract_alphanum, is_not_empty_array, is_true

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

KEYWORD_WAIT_TIME = int(os.environ['KEYWORD_WAIT_TIME'])

extractor = URLExtract()

def stream_keywoards(keyword, usernames):
    tso = TwitterSearchOrder() 
    tso.set_count(int(os.environ['TWITTER_MAX_RESULTS']))
    tso.set_keywords([keyword])
    
    try:
        for tweet in ts.search_tweets_iterable(tso):
            username = extract_alphanum(tweet['user']['name'])
            cache_key = "{}#{}".format(username, tweet['id_str'])
            cache_val = get_cache_value(cache_key)
            quiet_log_msg("DEBUG", "[twitter][stream_keywoards] found tweet with keyword = {}, cache: {} = {}, from {}".format(keyword, cache_key, cache_val, username))
            if username not in usernames or is_true(cache_val):
                continue
            timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').isoformat()

            content = "At {} - {}".format(timestamp, tweet['text'])
            urls = extractor.find_urls(content)
            if is_not_empty_array(urls):
                for url in urls:
                    try:
                        r = requests.get(url)
                        content = content.replace(url, re.sub("\/$", "", r.url))
                    except Exception as ue:
                        log_msg("INFO", "[twitter][stream_keywoards] problem finding source url: {}, e = {}".format(url, ue))

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
        sleep(KEYWORD_WAIT_TIME)
