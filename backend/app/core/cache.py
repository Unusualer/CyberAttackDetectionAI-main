from redis import asyncio as aioredis
from ..core.config import settings

class CacheManager:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.default_ttl = 300  # 5 minutes
        
    async def get(self, key: str) -> str:
        return await self.redis.get(key)
        
    async def set(self, key: str, value: str, ttl: int = None):
        await self.redis.set(key, value, ex=ttl or self.default_ttl)
        
    async def delete(self, key: str):
        await self.redis.delete(key) 