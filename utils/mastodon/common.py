import os

from mastodon import Mastodon
from utils.common import is_null_env

def is_mastodon_enabled():
    return not any(is_null_env(p) for p in ['MASTODON_BASE_URL', 'MASTODON_ACCESS_TOKEN'])

_MASTODON_CLIENT = None
MASTODON_BASE_URL = os.getenv('MASTODON_BASE_URL')
MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')

if is_mastodon_enabled():
    _MASTODON_CLIENT = Mastodon(
        access_token = MASTODON_ACCESS_TOKEN,
        api_base_url = MASTODON_BASE_URL
    )
