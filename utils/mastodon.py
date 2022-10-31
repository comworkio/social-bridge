from mastodon import Mastodon

import os
import re

from utils.common import is_not_empty

MASTODON_BASE_URL = os.getenv('MASTODON_BASE_URL')
MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')

mastodon = None

if is_not_empty(MASTODON_BASE_URL) and is_not_empty(MASTODON_ACCESS_TOKEN):
    mastodon = Mastodon(
        access_token = MASTODON_ACCESS_TOKEN,
        api_base_url = MASTODON_BASE_URL
    )

def toot (username, message):
    if is_not_empty(MASTODON_BASE_URL) and is_not_empty(MASTODON_ACCESS_TOKEN):
        mastodon.toot(re.sub("^At", "{} at".format(username), message))
