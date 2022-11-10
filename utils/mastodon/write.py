from utils.common import sn_message
from utils.logger import quiet_log_msg
from utils.mastodon.common import _MASTODON_CLIENT, is_mastodon_enabled

def toot (username, message):
    if is_mastodon_enabled() and None != _MASTODON_CLIENT:
        quiet_log_msg("DEBUG", "[mastodon][toot] Send message from {} : {}".format(username, message))
        _MASTODON_CLIENT.toot(sn_message(username, message))
