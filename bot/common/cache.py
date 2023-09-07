from cachetools import TTLCache

agent_cache = TTLCache(maxsize=100, ttl=60)
