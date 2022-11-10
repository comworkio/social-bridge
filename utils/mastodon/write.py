from utils.common import sn_message
from utils.mastodon.common import _MASTODON_CLIENT, is_mastodon_enabled

def toot (username, message):
    if is_mastodon_enabled() and None != _MASTODON_CLIENT:
        _MASTODON_CLIENT.toot(sn_message(username, message))
