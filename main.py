import os

from time import sleep

from utils.logger import log_msg, quiet_log_msg

from utils.twitter.read import stream_tweets

WAIT_TIME = int(os.environ['WAIT_TIME'])

log_msg("INFO", "[twitter-slack] deployment of version {} !".format(os.environ['TWITTER_SLACK_VERSION']))
while True:
    quiet_log_msg("INFO", "[main] reading tweets, WAIT_TIME = {}".format(WAIT_TIME))
    stream_tweets()
    sleep(WAIT_TIME)
