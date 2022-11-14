import os
import requests
import re

from datetime import datetime
from urlextract import URLExtract
from time import sleep

from utils.common import extract_alphanum, is_from_another_account, is_not_empty, is_not_empty_array

from utils.config import get_keywords, get_owners, get_usernames
from utils.logger import log_msg, quiet_log_msg
from utils.mastodon.write import toot
from utils.redis import get_cache_value, set_cache_value

from utils.slack import slack_messages
from utils.stream import is_twitter_primary_stream
from utils.twitter.common import _TWITTER_CLIENT, is_twitter_enabled
from utils.uprodit import send_uprodit

KEYWORD_WAIT_TIME = int(os.environ['KEYWORD_WAIT_TIME'])
TWITTER_RETENTION_DAYS = int(os.environ['TWITTER_RETENTION_DAYS'])
CACHE_KEY_TPL = "{}#{}"

_EXTRACTOR = URLExtract()

def diff_in_days(date):
    return (datetime.now().replace(tzinfo=None) - date.replace(tzinfo=None)).days

def exists_cache_entry(username, tweet):
    return is_not_empty(get_cache_value(CACHE_KEY_TPL.format(username, tweet['id'])))

def stream_keywoard(keyword, usernames, owners):
    if not is_twitter_enabled() or not is_twitter_primary_stream() or None == _TWITTER_CLIENT:
        log_msg("DEBUG", "[twitter][stream_keywoard] skipping...")
        return
    
    try:
        tweets = _TWITTER_CLIENT.search_recent_tweets(query=keyword, expansions = "author_id", user_fields = ['username'], tweet_fields=['created_at'], max_results=int(os.environ['TWITTER_MAX_RESULTS']))
        users = {u["id"]: u for u in tweets.includes['users']}
        for raw_tweet in tweets.data:
            username = extract_alphanum(users[raw_tweet.author_id]['username'])
            tweet = raw_tweet.data
            cache_key = CACHE_KEY_TPL.format(username, tweet['id'])
            
            quiet_log_msg("DEBUG", "[twitter][stream_keywoard] found tweet with keyword = {}, from {}".format(keyword, username))
            if not username in usernames or exists_cache_entry(username, tweet):
                continue
            
            timestamp = datetime.fromisoformat(tweet['created_at'])

            if is_from_another_account(tweet['text']):
                continue

            d = diff_in_days(timestamp)
            if d >= TWITTER_RETENTION_DAYS:
                quiet_log_msg("DEBUG", "[twitter][stream_keywoard] timestamp = {}, d = {} >= {}".format(timestamp.isoformat(), d, TWITTER_RETENTION_DAYS))
                continue

            if username in owners:
                content = tweet['text']
            else:
                content = "At {} - {}".format(timestamp.isoformat(), tweet['text'])
            
            urls = _EXTRACTOR.find_urls(content)
            if is_not_empty_array(urls):
                for url in urls:
                    try:
                        r = requests.get(url)
                        content = content.replace(url, re.sub("\/$", "", r.url))
                    except Exception as ue:
                        log_msg("INFO", "[twitter][stream_keywoard] problem finding source url: {}, e = {}".format(url, ue))

            quiet_log_msg("INFO", "[twitter][stream_keywoard] found tweet username = {}, content = {}".format(username, content))
            slack_messages(content, username, True)
            toot(username, content)
            send_uprodit(username, content, urls)
            set_cache_value(cache_key, "true")
    except Exception as e:
        log_msg("ERROR", "[twitter][stream_keywoard] unexpected error : {}".format(e))

def stream_tweets():
    if not is_twitter_enabled() or not is_twitter_primary_stream() or None == _TWITTER_CLIENT:
        log_msg("DEBUG", "[twitter][stream_tweets] skipping...")
        return

    keywords = get_keywords()
    usernames = get_usernames()
    owners = get_owners()
    quiet_log_msg("INFO", "[twitter][stream_tweets] searching tweet from usernames = {}, keywords = {}".format(usernames, keywords))
    for keyword in keywords:
        stream_keywoard(keyword, usernames, owners)
        sleep(KEYWORD_WAIT_TIME)
