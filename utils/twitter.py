import os
import requests
import re

from TwitterSearch import *
from datetime import datetime
from urlextract import URLExtract
from time import sleep

from utils.common import extract_alphanum, is_empty_array, is_not_empty, is_not_empty_array, is_not_null_env

from utils.config import get_keywords, get_owners, get_usernames
from utils.logger import log_msg, quiet_log_msg
from utils.mastodon import toot
from utils.redis import get_cache_value, set_cache_value

from utils.slack import slack_messages
from utils.stream import is_mastodon_primary_stream
from utils.uprodit import send_uprodit

def is_twitter_enabled():
    return not any(is_not_null_env(p) for p in ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET'])

ts = None
if is_twitter_enabled():
    ts = TwitterSearch (
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token = os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

KEYWORD_WAIT_TIME = int(os.environ['KEYWORD_WAIT_TIME'])
TWITTER_RETENTION_DAYS = int(os.environ['TWITTER_RETENTION_DAYS'])
CACHE_KEY_TPL = "{}#{}"

extractor = URLExtract()

def get_tus(tweet):
    tus = []
    if 'name' in tweet['user']:
        tus.append(extract_alphanum(tweet['user']['name']))
    if 'screen_name' in tweet['user']:
        tus.append(extract_alphanum(tweet['user']['screen_name']))
    return tus

def diff_in_days(date):
    return (datetime.now().replace(tzinfo=None) - date.replace(tzinfo=None)).days

def exists_cache_entry(tus, tweet):
    return is_not_empty(get_cache_value(CACHE_KEY_TPL.format(tus[0], tweet['id_str']))) or is_not_empty(get_cache_value(CACHE_KEY_TPL.format(tus[1], tweet['id_str'])))

def stream_keywoards(keyword, usernames, owners):
    if not is_twitter_enabled() or ts == None:
        log_msg("DEBUG", "[twitter][stream_keywoards] skipping...")
        return

    tso = TwitterSearchOrder() 
    tso.set_count(int(os.environ['TWITTER_MAX_RESULTS']))
    tso.set_keywords([keyword])
    
    try:
        for tweet in ts.search_tweets_iterable(tso):
            tus = get_tus(tweet)
            if is_empty_array(tus) and len(tus) < 2:
                continue

            username = tus[1]
            cache_key = CACHE_KEY_TPL.format(username, tweet['id_str'])
            
            quiet_log_msg("DEBUG", "[twitter][stream_keywoards] found tweet with keyword = {}, from {}".format(keyword, username))
            if not any(tu in usernames for tu in tus) or exists_cache_entry(tus, tweet):
                continue
            timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
            d = diff_in_days(timestamp)
            if d >= TWITTER_RETENTION_DAYS:
                quiet_log_msg("DEBUG", "[twitter][stream_keywoards] timestamp = {}, d = {} >= {}".format(timestamp.isoformat(), d, TWITTER_RETENTION_DAYS))
                continue

            if any(tu in owners for tu in tus):
                content = tweet['text']
            else:
                content = "At {} - {}".format(timestamp.isoformat(), tweet['text'])
            
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
            if not is_mastodon_primary_stream():
                toot(username, content)
            send_uprodit(username, content, urls)
            set_cache_value(cache_key, "true")
    except Exception as e:
        log_msg("ERROR", "[twitter][stream_keywoards] unexpected error : {}".format(e))

def stream_tweets():
    if not is_twitter_enabled() or ts == None:
        log_msg("DEBUG", "[twitter][stream_tweets] skipping...")
        return

    keywords = get_keywords()
    usernames = get_usernames()
    owners = get_owners()
    quiet_log_msg("INFO", "[twitter][stream_tweets] searching tweet from usernames = {}, keywords = {}".format(usernames, keywords))
    for keyword in keywords:
        stream_keywoards(keyword, usernames, owners)
        sleep(KEYWORD_WAIT_TIME)
