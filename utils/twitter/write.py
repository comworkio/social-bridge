import os
from utils.common import sn_message
from utils.logger import quiet_log_msg

from utils.twitter.common import _TWITTER_CLIENT, is_twitter_enabled

def tweet(username, message):
    if is_twitter_enabled() and None != _TWITTER_CLIENT:
        quiet_log_msg("DEBUG", "[twitter][tweet] Send message from {} : {}".format(username, message))
        _TWITTER_CLIENT.create_tweet(text = sn_message(username, message))
