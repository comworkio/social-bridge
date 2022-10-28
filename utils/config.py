import os

from utils.common import extract_alphanum, is_empty

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
        username = extract_alphanum(val)
        if username not in usernames:
            usernames.append(username)
        i = i+1
    return usernames
