import os
import pycurl
import json

from utils.slack import slack_messages
from utils.config import get_usernames

LOG_LEVEL = os.environ['LOG_LEVEL']
SLACK_TRIGGER = os.environ['SLACK_TRIGGER']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

def check_log_level ( log_level ):
    if LOG_LEVEL == "debug" or LOG_LEVEL == "DEBUG":
        return True
    else:
        return log_level != "debug" and log_level != "DEBUG"

def quiet_log_msg ( log_level, message ):
    if check_log_level(log_level):
        print ("[{}] {}".format(log_level, message))

def log_msg( log_level, message, is_public = False):
    if check_log_level(log_level):
        quiet_log_msg (log_level, message)
        slack_messages(message, get_usernames()[0], is_public)
