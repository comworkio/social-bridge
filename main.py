import os

from time import sleep

from utils.logger import log_msg, quiet_log_msg
from utils.mastodon.read import stream_toots

from utils.twitter.read import stream_tweets

WAIT_TIME = int(os.environ['WAIT_TIME'])

log_msg("INFO", "[social-bridge] deployment of version {} !".format(os.environ['SOCIAL_BRIDGE_VERSION']))
while True:
    quiet_log_msg("INFO", "[main] reading tweets and toots, WAIT_TIME = {}".format(WAIT_TIME))
    stream_tweets()
    stream_toots()
    sleep(WAIT_TIME)
