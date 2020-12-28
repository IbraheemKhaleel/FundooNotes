import redis
from decouple import config

r = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))        
        

class Cache:

    """
    Created a class to set and get the respective token in redis cache
    """
    
    @staticmethod
    def set_cache(key, value):
        """
        it takes key and value value as inputs and stores it in redis server and has expiry time of 60 seconds
        """
        r.set(key, value)
        r.expire(key, time=60)

    @staticmethod
    def get_cache(key):
        """
        it takes key as input and returns value stored with that key
        """
        return r.get(key)