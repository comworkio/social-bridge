from time import sleep
import os
from utils.logger import quiet_log_msg

from utils.twitter import stream_tweets

WAIT_TIME = int(os.environ['WAIT_TIME'])

while True:
    quiet_log_msg("INFO", "[main] reading tweets, WAIT_TIME = {}".format(WAIT_TIME))
    stream_tweets()
    sleep(WAIT_TIME)
