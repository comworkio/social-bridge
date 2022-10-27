import os
import pycurl
import json

from utils.common import is_empty

def slack_message ( message , token , username):
    if SLACK_TRIGGER == 'on':
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://hooks.slack.com/services/{}".format(token))
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        c.setopt(pycurl.POST, 1)
        data = json.dumps({"text": message, "username": username, "channel": SLACK_CHANNEL, "icon_emoji": ":{}:".format(username) })
        c.setopt(pycurl.POSTFIELDS, data)
        c.perform()

def slack_messages( message , username , is_public):
        slack_message(message, os.environ['SLACK_TOKEN'], username)
        if is_public:
            i = 1
            while True:
                token_val = os.getenv("SLACK_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    break
                slack_message(message, token_val, username)
                i = i+1
