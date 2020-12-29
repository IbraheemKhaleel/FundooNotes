import redis
from decouple import config
       
        
#cache
class Cache:

    """
    Created a class to set and get the respective token in redis cache
    """
    def __init__(self):
        self.r = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))   

    
   
    def set_cache(self, key, value):
        """
        it takes key and value value as inputs and stores it in redis server and has expiry time of 60 seconds
        """
        self.r.set(key, value)
        self.r.expire(key, time=60)

    
    def get_cache(self, key):
        """
        it takes key as input and returns value stored with that key
        """
        return self.r.get(key)