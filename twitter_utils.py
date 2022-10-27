from TwitterSearch import *
from datetime import datetime

import os

from common_utils import *

ts = TwitterSearch (
    consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
    access_token = os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

def get_ts():
    return ts
