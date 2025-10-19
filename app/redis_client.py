import redis
import json
import os
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        self.redis_host = os.getenv("REDIS_HOST", "api.redis")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_client: Optional[redis.Redis] = None
        self.enabled = True
        self._connect()
    
    def _connect(self):
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=0,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self.enabled = False
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                logger.info(f"Cache hit: {key}")
                return json.loads(value)
            logger.info(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized)
            logger.info(f"Cached: {key} (TTL: {ttl}s)")
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
    
    def delete(self, key: str):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.delete(key)
            logger.info(f"Deleted from cache: {key}")
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
    
    def clear(self):
        if not self.enabled or not self.redis_client:
            return
        
        try:
            self.redis_client.flushdb()
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def get_stats(self) -> dict:
        if not self.enabled or not self.redis_client:
            return {"enabled": False, "status": "disabled"}
        
        try:
            info = self.redis_client.info()
            return {
                "enabled": True,
                "status": "connected",
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"enabled": False, "status": "error", "error": str(e)}
    
    def health_check(self) -> bool:
        """Check Redis connection health"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            return self.redis_client.ping()
        except Exception:
            return False

