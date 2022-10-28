from ast import keyword
from TwitterSearch import *
from datetime import datetime
from utils.common import extract_username, is_empty

import os
from utils.logger import quiet_log_msg

from utils.slack import slack_messages

ts = TwitterSearch (
    consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
    access_token = os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

def get_keywords():
    i = 1
    keywords = []
    while True:
        keyword = os.getenv("TWITTER_KEYWORD_{}".format(i))
        if is_empty(keyword):
            break
        if keyword not in keywords:
            keywords.append(keyword)
        i = i+1
    return keywords

def get_usernames():
    i = 1
    usernames = []
    while True:
        val = os.getenv("TWITTER_USERNAME_{}".format(i))
        if is_empty(val):
            break
        username = extract_username(val)
        if username not in usernames:
            usernames.append(username)
        i = i+1
    return usernames

def read_tweets():
    tso = TwitterSearchOrder() 
    tso.set_count(int(os.environ['TWITTER_MAX_RESULTS']))
    keywords = get_keywords()
    usernames = get_usernames()
    quiet_log_msg("INFO", "searching tweet from usernames = {}, keywords = {}".format(usernames, keywords))
    tso.set_keywords(keywords)
    for tweet in ts.search_tweets_iterable(tso):
        username = extract_username(tweet['user']['name'])
        quiet_log_msg("DEBUG", "found tweet from {}".format(username))
        if username not in usernames:
            continue
        timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').isoformat()
        content = "[{}] {}".format(timestamp, tweet['text'])
        quiet_log_msg("INFO", "found tweet username = {}, content = {}".format(username, content))
        slack_messages(content, username, True)
