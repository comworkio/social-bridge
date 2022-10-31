from hashlib import sha1
from uuid import uuid4
from time import time
from base64 import encodebytes
from urllib.parse import quote

import hmac
import re
import os

UPRODIT_API_URL = os.environ['UPRODIT_API_URL']
UPRODIT_APPID = os.getenv('UPRODIT_APPID')
UPRODIT_ENV = os.getenv('UPRODIT_ENV')
UPRODIT_USERNAME = os.getenv('UPRODIT_USERNAME')
UPRODIT_PASSWORD = os.getenv('UPRODIT_PASSWORD')
UPRODIT_PROFILE_ID = os.getenv('UPRODIT_PROFILE_ID')

UPRODIT_NEWSPAPER_API = "{}/v1/post"

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

def send_uprodit(username, message):
