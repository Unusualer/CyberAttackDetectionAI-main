from fastapi import Request
from ..services.cache import RedisCache
from ..core.config import settings
import hashlib

class CacheMiddleware:
    def __init__(self):
        self.cache = RedisCache()
        self.cache_enabled_paths = {
            "/api/v1/organizations": ["GET"],
            "/api/v1/agents": ["GET"],
            "/api/v1/events": ["GET"],
        }

    def _should_cache(self, request: Request) -> bool:
        """Check if request should be cached"""
        if request.method not in ["GET"]:
            return False
            
        return any(
            path in request.url.path
            for path in self.cache_enabled_paths
            if request.method in self.cache_enabled_paths[path]
        )

    def _generate_cache_key(self, request: Request) -> str:
        """Generate unique cache key for request"""
        key_parts = [
            request.url.path,
            str(request.query_params),
            request.headers.get("authorization", "")
        ]
        return hashlib.md5(
            "|".join(key_parts).encode()
        ).hexdigest()

    async def __call__(self, request: Request, call_next):
        if not self._should_cache(request):
            return await call_next(request)

        cache_key = self._generate_cache_key(request)
        
        # Try to get from cache
        cached_response = await self.cache.get(cache_key)
        if cached_response is not None:
            return JSONResponse(content=cached_response)

        # Get fresh response
        response = await call_next(request)
        
        # Cache the response
        if response.status_code == 200:
            await self.cache.set(
                cache_key,
                response.body,
                settings.CACHE_TTL
            )

        return response 