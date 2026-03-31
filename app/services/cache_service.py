
from cachetools import TTLCache

ticker_cache = TTLCache(maxsize=100, ttl=10)
ohlcv_cache = TTLCache(maxsize=100, ttl=60)

class CacheService:
    @staticmethod
    def get(cache, key):
        return cache.get(key)

    @staticmethod
    def set(cache, key, value):
        cache[key] = value