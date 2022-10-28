import os
import pycurl
import json

from utils.common import is_empty, is_true

SLACK_TRIGGER = os.environ['SLACK_TRIGGER']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_TOKEN = os.environ['SLACK_TOKEN']

def slack_message ( message , token , username):
    if is_true(SLACK_TRIGGER):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://hooks.slack.com/services/{}".format(token))
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        c.setopt(pycurl.POST, 1)
        data = json.dumps({"text": message, "username": username, "channel": SLACK_CHANNEL, "icon_emoji": ":{}:".format(username) })
        c.setopt(pycurl.POSTFIELDS, data)
        c.perform()

def slack_messages( message , username , is_public):
        slack_message(message, SLACK_TOKEN, username)
        if is_public:
            i = 1
            while True:
                token_val = os.getenv("SLACK_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    break
                slack_message(message, token_val, username)
                i = i+1
