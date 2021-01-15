import redis
from decouple import config


class Cache:

    def __init__(self):
        self.r = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))

    def set_cache(self, key, value):
        """
        takes key[id] and value[token] value as inputs and stores it in redis server and has expiration time of 60 seconds
        """
        self.r.set(key, value)
        self.r.expire(key, time=8000)

    def get_cache(self, key):
        """
        it takes key as input and returns value stored with that key
        """
        return self.r.get(key)

    def delete_cache(self, key):
        """
        @param key: The key of the respective note
        @type key: String
        """
        self.r.delete(key)
