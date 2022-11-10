import requests
import os
import html2text

from datetime import datetime
from urlextract import URLExtract
from utils.common import extract_alphanum, is_empty, is_not_empty, is_not_null_property
from utils.config import get_keywords, get_owners, get_usernames
from utils.logger import log_msg, quiet_log_msg
from utils.mastodon.common import MASTODON_BASE_URL
from utils.redis import get_cache_value, set_cache_value
from utils.slack import slack_messages
from utils.stream import is_mastodon_primary_stream
from utils.twitter.read import diff_in_days
from utils.twitter.write import tweet
from utils.uprodit import send_uprodit

TWITTER_RETENTION_DAYS = int(os.environ['TWITTER_RETENTION_DAYS'])
CACHE_KEY_TPL = "mastodon#{}#{}"

LIMIT = 40
plimit = os.getenv('TWITTER_MAX_RESULTS')
if is_not_empty(plimit) and int(plimit) <= LIMIT:
    LIMIT = int(plimit)

TIMELINE_TAG_URL = None
if is_not_null_property(MASTODON_BASE_URL):
    TIMELINE_TAG_URL = "{}/api/v1/timelines/tag".format(MASTODON_BASE_URL)

if is_not_empty(TIMELINE_TAG_URL) and not TIMELINE_TAG_URL.startswith("http"):
    TIMELINE_TAG_URL = "https://{}".format(TIMELINE_TAG_URL)

_H = html2text.HTML2Text()
_H.ignore_links = True

_EXTRACTOR = URLExtract()

def format_toot(content):
    return _H.handle(content).replace("\n", " ")

def exists_cache_entry(username, toot):
    return is_not_empty(get_cache_value(CACHE_KEY_TPL.format(username, toot['id'])))

def stream_keyword(keyword, usernames, owners):
    if not is_mastodon_primary_stream():
        log_msg("DEBUG", "[mastodon][stream_keywoard] skipping...")
        return

    r = requests.get("{}/{}?limit={}".format(TIMELINE_TAG_URL, keyword, LIMIT))
    try:
        toots = r.json()
        for toot in toots:
            username = extract_alphanum(toot['account']['username'])
            cache_key = CACHE_KEY_TPL.format(username, toot['id'])
            if not username in usernames or exists_cache_entry(username, toot):
                continue

            content = format_toot(toot['content'])
            if content.startswith("From {} at".format(username)):
                continue

            timestamp = datetime.fromisoformat(toot['created_at'])

            if username in owners:
                content = content
            else:
                content = "At {} - {}".format(timestamp.isoformat(), content)

            d = diff_in_days(timestamp)
            if d >= TWITTER_RETENTION_DAYS:
                quiet_log_msg("DEBUG", "[mastodon][stream_keywoards] timestamp = {}, d = {} >= {}".format(timestamp.isoformat(), d, TWITTER_RETENTION_DAYS))
                continue

            quiet_log_msg("INFO", "[mastodon][stream_keyword] found tweet username = {}, content = {}".format(username, content))
            slack_messages(content, username, True)
            send_uprodit(username, content, _EXTRACTOR.find_urls(content))
            tweet(username, content)

            set_cache_value(cache_key, "true")
    except Exception as e:
        log_msg("ERROR", "[mastodon][stream_keyword] unexpected error : {}".format(e))

def stream_toots():
    if is_empty(TIMELINE_TAG_URL) or not is_mastodon_primary_stream():
        log_msg("DEBUG", "[mastodon][stream_toots] skipping...")
        return

    usernames = get_usernames()
    owners = get_owners()
    for keyword in get_keywords():
        stream_keyword(keyword, usernames, owners)
