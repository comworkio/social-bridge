from mastodon import Mastodon

import os
import re

from utils.common import is_not_null_property, sn_message

MASTODON_BASE_URL = os.getenv('MASTODON_BASE_URL')
MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')

mastodon = None

if is_not_null_property(MASTODON_BASE_URL) and is_not_null_property(MASTODON_ACCESS_TOKEN):
    mastodon = Mastodon(
        access_token = MASTODON_ACCESS_TOKEN,
        api_base_url = MASTODON_BASE_URL
    )

def toot (username, message):
    if is_not_null_property(MASTODON_BASE_URL) and is_not_null_property(MASTODON_ACCESS_TOKEN):
        mastodon.toot(sn_message(message))
