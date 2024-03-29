import os
import requests

from utils.common import is_disabled, is_empty, is_enabled, is_not_empty, is_true
from utils.logger import DISCORD_WEBHOOK_TPL, SLACK_WEBHOOK_TPL, is_notif_enabled, log_msg

SLACK_TRIGGER = os.getenv('SLACK_TRIGGER')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ENABLE_MATCHING = os.getenv('DISCORD_ENABLE_MATCHING')
CUSTOM_ALERT_URL = os.getenv('CUSTOM_ALERT_URL')

def notif_message(payload, token, webhook_tpl, channel):
    if not is_notif_enabled():
        return

    notif_url(payload, webhook_tpl.format(token), channel)

def notif_url(payload, url, channel):
    if is_empty(url):
        return

    n_payload = { "username": payload['username'] }

    if "color" in payload and "title" in payload:
        n_payload['attachments'] = [{
            "text": payload['message'], 
            "color": payload['color'], 
            "title": payload['title'] 
        }]
    elif "color" in payload:
        n_payload['attachments'] = [{
            "text": payload['message'], 
            "color": payload['color'] 
        }]
    elif "title" in payload:
        n_payload['attachments'] = [{
            "text": payload['message'], 
            "title": payload['title'] 
        }]
    else:
        n_payload['message'] = payload['message']

    if "discord" not in url:
        n_payload['channel'] = channel
        n_payload['icon_emoji'] = ":{}:".format(payload['username'])

    try:
        log_msg("DEBUG", "[notif_message] send payload to webhook {}: {}".format(url, n_payload))
        r = requests.post(url, json = n_payload)
        if not (r.status_code >= 200 and r.status_code < 400):
            log_msg("ERROR", "[notif_message] webhook respond with error: code = {}, body = {}".format(r.status_code, r.content))

    except Exception as e:
        log_msg("ERROR", "[notif_message] exception occured posting on this url = {}, e = {}".format(url, e))

def broadcast_messages(payload, is_public, channel_key):
    channel = os.getenv(channel_key)
    if is_disabled(channel):
        log_msg("WARN", "[broadcast_messages] there's no channel environment variable")
        return

    if is_enabled(SLACK_TOKEN):
        notif_message(payload, SLACK_TOKEN, SLACK_WEBHOOK_TPL, channel)
    
    if is_enabled(DISCORD_TOKEN):
        notif_message(payload, DISCORD_TOKEN, DISCORD_WEBHOOK_TPL, channel)

    notif_url(payload, CUSTOM_ALERT_URL, channel)

    if is_public:
        i = 0
        while True:
            token_val = os.getenv("SLACK_PUBLIC_TOKEN_{}".format(i))
            if is_empty(token_val) and i > 0:
                log_msg("DEBUG", "[broadcast_messages] no more token, i = {}".format(i))
                break
            notif_message(payload, token_val, SLACK_WEBHOOK_TPL, channel)
            i = i + 1

        if is_true(DISCORD_ENABLE_MATCHING):
            token_key = "DISCORD_{}_TOKEN".format(channel.upper().replace("-", "").replace("#", ""))
            token_val = os.getenv(token_key)
            if is_not_empty(token_val):
                notif_message(payload, token_val, DISCORD_WEBHOOK_TPL, channel)
        else:
            i = 0
            while True:
                token_val = os.getenv("DISCORD_PUBLIC_TOKEN_{}".format(i))
                if is_empty(token_val):
                    if i <= 0:
                        i = i + 1
                        continue
                    else:
                        log_msg("DEBUG", "[broadcast_messages] no more token, i = {}".format(i))
                        break
                notif_message(payload, token_val, DISCORD_WEBHOOK_TPL, channel)
                i = i + 1

def notif_messages(payload, is_public):
    return broadcast_messages(payload, is_public, 'SLACK_CHANNEL')

def incident_message(payload):
    return broadcast_messages(payload, True, 'PROD_CHANNEL')
