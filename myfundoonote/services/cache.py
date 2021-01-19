import redis
from decouple import config


class Cache:
    """
    Instantiates cache object and returns same instance for further operations using getInstance()
    """

    __shared_instance = None

    @staticmethod
    def getInstance():
        """[returns initialised cache instance to calling view]
        :return: cache instance stored in __shared_instance
        """

        if Cache.__shared_instance is None:
            Cache.__shared_instance = Cache(config('REDIS_HOST'), config('REDIS_PORT'))
        return Cache.__shared_instance

    def __init__(self, host, port):
        """
        Constructor to initialize the host and port of redis server
       @param host: host of the port
       @type host: string
       @param port: Number of the port
       @type port: Int
       """

        self.cache = redis.StrictRedis(host=host, port=port)

    def set_cache(self, key, value):
        """

        @param key: key value of the respective value
        @type key: string
        @param value: value of the element we storing in cache
        @type value: string
        """
        self.cache.set(key, value)
        self.cache.expire(key, time=60000)

    def get_cache(self, key):
        """[gets value for existing key in cache]
        :param key: [mandatory]:[string]:the key to be used for existing token/note record
        :return: value stored against key
        """
        return self.cache.get(key)

    def delete_cache(self, key):
        """[deletes cache record for existing key in cache]
        :param key: :[string]:the key to be used for existing token/note record
        """
        self.cache.delete(key)
