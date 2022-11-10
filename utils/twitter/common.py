from utils.common import is_null_env

def is_twitter_enabled():
    return not any(is_null_env(p) for p in ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET', 'TWITTER_BEARER_TOKEN'])
