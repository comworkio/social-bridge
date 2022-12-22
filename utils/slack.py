import os
import requests

from utils.common import is_empty, is_not_empty, is_not_null_property, is_null_property, is_true

SLACK_TRIGGER = os.getenv('SLACK_TRIGGER')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ENABLE_MATCHING = os.getenv('DISCORD_ENABLE_MATCHING')

SLACK_WEBHOOK_TPL = "https://hooks.slack.com/services/{}"
DISCORD_WEBHOOK_TPL = "https://discord.com/api/webhooks/{}/slack"

def slack_message ( message , token , username, webhook_tpl, channel):
    if is_not_null_property(SLACK_TRIGGER) and is_true(SLACK_TRIGGER):
        url = webhook_tpl.format(token)
        payload = {"text": message, "username": username }

        if "discord" not in webhook_tpl:
            payload['channel'] = channel
            payload['icon_emoji'] = ":{}:".format(username)

        try:
            requests.post(url, json = payload)
        except Exception as e:
            print("[INFO][slack][slack_message] exception occured posting on this url = {}, e = {}".format(url, e))

def broadcast_messages( message , username , is_public, channel_key):
    channel = os.getenv(channel_key)
    if is_null_property(channel):
        return

    if is_not_null_property(SLACK_TOKEN):
        slack_message(message, SLACK_TOKEN, username, SLACK_WEBHOOK_TPL, channel)
    
    if is_not_null_property(DISCORD_TOKEN):
        slack_message(message, DISCORD_TOKEN, username, DISCORD_WEBHOOK_TPL, channel)

    if is_public:
        i = 1
        while True:
            token_val = os.getenv("SLACK_PUBLIC_TOKEN_{}".format(i))
            if is_empty(token_val):
                break
            slack_message(message, token_val, username, SLACK_WEBHOOK_TPL, channel)
            i = i + 1

        if is_true(DISCORD_ENABLE_MATCHING):
            token_val = os.getenv("DISCORD_{}_TOKEN".format(channel))
            if is_not_empty(token_val):
                slack_message(message, token_val, username, DISCORD_WEBHOOK_TPL, channel)
        else:
            i = 1
            while True:
                token_val = os.getenv("DISCORD_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    break
                slack_message(message, token_val, username, DISCORD_WEBHOOK_TPL, channel)
                i = i + 1

def slack_messages( message , username , is_public):
    return broadcast_messages(message, username, is_public, 'SLACK_CHANNEL')

def incident_message( message , username ):
    return broadcast_messages(message, username, True, 'PROD_CHANNEL')
