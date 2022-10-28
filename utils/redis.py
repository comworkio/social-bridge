import redis
import os

from utils.logger import quiet_log_msg

TTL = int(os.environ['REDIS_TTL'])
r = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=0)

def get_cache_value(key):
    quiet_log_msg("DEBUG", "[redis][get_cache_value] accessing key={}".format(key))
    return r.get(key)

def set_cache_value(key, value):
    quiet_log_msg("INFO", "[redis][set_cache_value] storing key={}, value={}, ttl={}".format(key, value, TTL))
    return r.set(key, value, ex=TTL)
