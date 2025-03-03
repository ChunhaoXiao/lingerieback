import redis
from core.config import Setting
redis_client = redis.Redis(host=Setting.REDIS_HOST, port=6379, db=0,charset="utf-8", decode_responses=True)

def set_config(key, val):
    redis_client.set(key, val)
    
def get_config(key):
    return redis_client.get(key)