import os
import pycurl
import json

from utils.common import is_empty

LOG_LEVEL = os.environ['LOG_LEVEL']
SLACK_TRIGGER = os.environ['SLACK_TRIGGER']

def slack_message ( message , token):
    if SLACK_TRIGGER == 'on':
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://hooks.slack.com/services/{}".format(token))
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        c.setopt(pycurl.POST, 1)
        data = json.dumps({"text": message, "username": os.environ['SLACK_USERNAME'], "channel": os.environ['SLACK_CHANNEL'], "icon_emoji": os.environ['SLACK_EMOJI'] })
        c.setopt(pycurl.POSTFIELDS, data)
        c.perform()

def slack_messages( message , is_public):
        slack_message(message, os.environ['SLACK_TOKEN'])
        if is_public:
            i = 1
            while True:
                token_val = os.getpid("SLACK_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    break
                slack_message(message, token_val)
                i = i+1

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
        slack_messages(message, is_public)
