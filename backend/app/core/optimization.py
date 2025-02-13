from functools import lru_cache
from typing import Any, Dict
import orjson

class CacheConfig:
    """Cache configuration for different components"""
    MODEL_CACHE_TTL = 3600  # 1 hour
    THREAT_INTEL_TTL = 1800  # 30 minutes
    MAX_CACHE_ITEMS = 1000

def optimize_json_serialization(data: Dict[str, Any]) -> bytes:
    """Optimized JSON serialization using orjson"""
    return orjson.dumps(
        data,
        option=orjson.OPT_SERIALIZE_NUMPY | 
               orjson.OPT_SERIALIZE_DATETIME |
               orjson.OPT_SORT_KEYS
    )

@lru_cache(maxsize=CacheConfig.MAX_CACHE_ITEMS)
def get_cached_threat_patterns(pattern_id: str) -> Dict[str, Any]:
    """Cache frequently used threat patterns"""
    # Implementation 