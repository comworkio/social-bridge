import os

from utils.common import is_not_null_property
from utils.logger import quiet_log_msg

def is_mastodon_primary_stream():
    primary_stream = os.getenv('STREAM_PRIMARY_SRC')
    quiet_log_msg("DEBUG", "[is_mastodon_primary_stream] primary_stream = {}".format(primary_stream))
    return is_not_null_property(primary_stream) and "mastodon" == primary_stream.lower()
