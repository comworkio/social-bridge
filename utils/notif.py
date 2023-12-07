import os
import requests

from utils.common import is_empty, is_not_empty, is_not_null_property, is_null_property, is_true
from utils.logger import DISCORD_WEBHOOK_TPL, SLACK_WEBHOOK_TPL, is_notif_enabled, log_msg

SLACK_TRIGGER = os.getenv('SLACK_TRIGGER')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ENABLE_MATCHING = os.getenv('DISCORD_ENABLE_MATCHING')

def notif_message(payload, token, webhook_tpl, channel):
    if not is_notif_enabled():
        return

    url = webhook_tpl.format(token)
    npayload = { "username": payload['username'] }

    if "color" in payload and "title" in payload:
        npayload['attachments']: [{ "text": payload['message'], "color": payload['color'], "title": payload['title'] }]
    elif "color" in payload:
        npayload['attachments']: [{ "text": payload['message'], "color": payload['color'] }]
    elif "title" in payload:
        npayload['attachments']: [{ "text": payload['message'], "title": payload['title'] }]
    else:
        npayload['message'] = payload['message']

    if "discord" not in webhook_tpl:
        npayload['channel'] = channel
        npayload['icon_emoji'] = ":{}:".format(payload['username'])

    try:
        requests.post(url, json = npayload)
    except Exception as e:
        log_msg("ERROR", "[notif_message] exception occured posting on this url = {}, e = {}".format(url, e))

def broadcast_messages(payload, is_public, channel_key):
    channel = os.getenv(channel_key)
    if is_null_property(channel):
        return

    if is_not_null_property(SLACK_TOKEN):
        notif_message(payload, SLACK_TOKEN, SLACK_WEBHOOK_TPL, channel)
    
    if is_not_null_property(DISCORD_TOKEN):
        notif_message(payload, DISCORD_TOKEN, DISCORD_WEBHOOK_TPL, channel)

    if is_public:
        i = 1
        while True:
            token_val = os.getenv("SLACK_PUBLIC_TOKEN_{}".format(i))
            if is_empty(token_val):
                break
            notif_message(payload, token_val, SLACK_WEBHOOK_TPL, channel)
            i = i + 1

        if is_true(DISCORD_ENABLE_MATCHING):
            token_key = "DISCORD_{}_TOKEN".format(channel.upper().replace("-", "").replace("#", ""))
            token_val = os.getenv(token_key)
            if is_not_empty(token_val):
                notif_message(payload, token_val, DISCORD_WEBHOOK_TPL, channel)
        else:
            i = 1
            while True:
                token_val = os.getenv("DISCORD_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    break
                notif_message(payload, token_val, DISCORD_WEBHOOK_TPL, channel)
                i = i + 1

def notif_messages(payload, is_public):
    return broadcast_messages(payload, is_public, 'SLACK_CHANNEL')

def incident_message(payload):
    return broadcast_messages(payload, True, 'PROD_CHANNEL')
