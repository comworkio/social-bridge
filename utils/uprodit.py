from hashlib import sha1
from uuid import uuid4
from time import time
from base64 import encodebytes
from urllib.parse import quote

import hmac
import re
import os
import requests

from utils.common import is_empty, is_not_empty, is_not_empty_array, sn_message
from utils.logger import log_msg
from utils.redis import get_cache_value, set_cache_value

UPRODIT_API_URL = os.environ['UPRODIT_API_URL']
UPRODIT_APPID = os.getenv('UPRODIT_APPID')
UPRODIT_ENV = os.getenv('UPRODIT_ENV')
UPRODIT_USERNAME = os.getenv('UPRODIT_USERNAME')
UPRODIT_PASSWORD = os.getenv('UPRODIT_PASSWORD')
UPRODIT_PROFILE_ID = os.getenv('UPRODIT_PROFILE_ID')

UPRODIT_TOKEN_API = "{}/v1/token".format(UPRODIT_API_URL)
UPRODIT_NEWSPAPER_API = "{}/v1/post".format(UPRODIT_API_URL)

UPRODIT_CACHE_TOKEN_KEY = "uprodit_token_key"

def hmacsha1(key, raw):
    hashed = hmac.new(str.encode(key), str.encode(raw), sha1)
    return encodebytes(hashed.digest()).decode('utf-8').rstrip('\n')

def generate_signature (appid, env, uri):
    auth_signature_method = 'HMAC-SHA1'
    auth_consumer_key = quote(hmacsha1(appid, env))
    auth_token = uuid4()
    uri_path = re.sub("http(s)?://[^/]*", "", uri)
    auth_signature = quote(hmacsha1(appid, "{}{}".format(uri_path, auth_token)))
    auth_nonce = quote(hmacsha1(appid, "{}".format(uuid4())))
    auth_callback = quote(uri_path)
    auth_timestamp = time()
    return "Auth ?auth_signature={}&auth_nonce={}&auth_callback={}&auth_timestamp={}&auth_token={}&auth_signature_method={}&auth_consumer_key={}".format(auth_signature, auth_nonce, auth_callback, auth_timestamp, auth_token, auth_signature_method, auth_consumer_key)

def get_token():
    token = get_cache_value(UPRODIT_CACHE_TOKEN_KEY)
    if is_not_empty(token):
        return token

    payload = {"username": UPRODIT_USERNAME, "password": UPRODIT_PASSWORD}
    headers = {"Authorization": generate_signature(UPRODIT_APPID, UPRODIT_ENV, UPRODIT_TOKEN_API)}
    r = requests.post(UPRODIT_TOKEN_API, json = payload, headers = headers)
    if r.status_code != 200:
        log_msg("ERROR", "[get_token] authentication error : username = {}, code = {}".format(UPRODIT_USERNAME, r.status_code))
        return None

    token = r.json()['token']
    set_cache_value(UPRODIT_CACHE_TOKEN_KEY, token)
    return token

def send_uprodit(username, message, urls):
    content = sn_message(username, message)
    payload = {"idProfilPost": UPRODIT_PROFILE_ID, "descriptionPost": content}
    uprodit_token = get_token()

    if is_empty(uprodit_token):
        return

    if is_not_empty_array(urls):
        payload['link'] = urls[0]

    headers = {"Authorization": generate_signature(UPRODIT_APPID, UPRODIT_ENV, UPRODIT_NEWSPAPER_API), "x-uprodit-token": uprodit_token}
    requests.post(UPRODIT_NEWSPAPER_API, json = payload, headers = headers)
