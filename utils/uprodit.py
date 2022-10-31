from hashlib import sha1
from urllib.parse import quote
from uuid import uuid4
from time import time

import hmac
import re

def hmacsha1(key, raw):
    hashed = hmac.new(key, raw, sha1)
    return hashed.digest().encode("base64").rstrip('\n')

def generate_signature (appid, env, uri):
    auth_signature_method = 'HMAC-SHA1'
    auth_consumer_key = hmacsha1(appid, env)
    auth_token = uuid4()
    uri_path = re.sub("http(s)?://[^/]*", "", uri)
    auth_signature = quote(hmacsha1(appid, uri_path + auth_token))
    auth_nonce = quote(hmacsha1(appid, uuid4()))
    auth_callback = quote(uri_path)
    auth_timestamp = time()
    return "Auth ?auth_signature={}&auth_nonce={}&auth_callback={}&auth_timestamp={}&auth_token={}&auth_signature_method={}&auth_consumer_key={}".format(auth_signature, auth_nonce, auth_callback, auth_timestamp, auth_token, auth_signature_method, auth_consumer_key)

print(generate_signature("challenge_uprodit", "production", "https://api.uprodit.com/v2/profile/personal/en/51"))

