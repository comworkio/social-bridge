import redis
import os

TTL = os.environ['REDIS_TTL']
r = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=0)

def get_cache_value(key):
    return r.get(key)

def set_cache_value(key, value):
    return r.set(key, value, ex=TTL)
