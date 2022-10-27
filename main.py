from time import sleep
import os

from utils.twitter import read_tweets

WAIT_TIME = int(os.environ['WAIT_TIME'])

while True:
    read_tweets()
    sleep(WAIT_TIME)
