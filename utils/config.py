import os

from utils.common import extract_alphanum, is_empty

def get_list_configs(key_prefix, format):
    i = 1
    list_values = []
    while True:
        value = os.getenv("{}_{}".format(key_prefix, i))
        if is_empty(value):
            break
        formated_val = format(value)
        if formated_val not in list_values:
            list_values.append(formated_val)
        i = i+1
    return list_values

def get_keywords():
    return get_list_configs("TWITTER_KEYWORD", lambda x: x)

def get_owners():
    return get_list_configs("TWITTER_OWNER", extract_alphanum)

def get_usernames():
    return get_list_configs("TWITTER_USERNAME", extract_alphanum)
