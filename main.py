from time import sleep
import os
from utils.logger import quiet_log_msg

from utils.twitter import read_tweets

WAIT_TIME = int(os.environ['WAIT_TIME'])

while True:
    quiet_log_msg("INFO", "Reading tweets, WAIT_TIME = {}".format(WAIT_TIME))
    read_tweets()
    sleep(WAIT_TIME)
