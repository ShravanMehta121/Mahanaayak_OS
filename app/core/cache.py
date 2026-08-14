import json
import time

class SimpleMemoryCache:
    """Fallback in-memory cache if Redis is not available."""
    def __init__(self):
        self.store = {}
        
    def get(self, key):
        if key in self.store:
            data, expiry = self.store[key]
            if expiry is None or expiry > time.time():
                return data
            else:
                del self.store[key]
        return None
        
    def set(self, key, value, ex=None):
        expiry = time.time() + ex if ex else None
        self.store[key] = (value, expiry)
        
    def delete(self, key):
        if key in self.store:
            del self.store[key]

# Attempt to import redis, fallback to SimpleMemoryCache
try:
    import redis
    import os
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        _cache_client = redis.from_url(redis_url)
    else:
        _cache_client = SimpleMemoryCache()
except ImportError:
    _cache_client = SimpleMemoryCache()

class Cache:
    """Redis-ready Cache Interface"""
    
    @staticmethod
    def get(key):
        val = _cache_client.get(key)
        if val:
            # Redis returns bytes, MemoryCache returns strings/dicts
            if isinstance(val, bytes):
                return json.loads(val.decode('utf-8'))
            if isinstance(val, str):
                return json.loads(val)
            return val
        return None
        
    @staticmethod
    def set(key, value, timeout=300):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        _cache_client.set(key, value, ex=timeout)
        
    @staticmethod
    def delete(key):
        _cache_client.delete(key)
