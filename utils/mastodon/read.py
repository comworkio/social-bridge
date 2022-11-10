from utils.logger import log_msg
from utils.mastodon.common import _MASTODON_CLIENT
from utils.mastodon.common import is_mastodon_enabled

def stream_toots():
    if not is_mastodon_enabled():
        log_msg("DEBUG", "[mastodon][stream_toots] skipping...")
        return
    results = _MASTODON_CLIENT.search("techwatch")
    log_msg("DEBUG", "[mastodon][stream_toots] results = {}".format(results))
