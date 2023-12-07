import os

from utils.common import is_enabled
from utils.logger import quiet_log_msg

def is_mastodon_primary_stream():
    primary_stream = os.getenv('STREAM_PRIMARY_SRC')
    quiet_log_msg("DEBUG", "[is_mastodon_primary_stream] primary_stream = {}".format(primary_stream))
    return is_enabled(primary_stream) and "mastodon" == primary_stream.lower()

def is_twitter_primary_stream():
    return not is_mastodon_primary_stream()
