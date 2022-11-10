import os

from utils.common import is_not_null_property

def is_mastodon_primary_stream():
    primary_stream = os.get_env('STREAM_PRIMARY_SRC')
    return is_not_null_property(primary_stream) and "mastodon" == primary_stream.lower()
