"""Redis service for caching and memory."""

import redis.asyncio as redis
from typing import Optional, Any
import json

from app.core.config import settings


class RedisService:
    """Redis service for caching and memory management."""
    
    def __init__(self):
        """Initialize Redis connection."""
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self.client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis."""
        if not self.client:
            await self.connect()
        
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, expiry: Optional[int] = None):
        """Set value in Redis."""
        if not self.client:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if expiry:
            await self.client.setex(key, expiry, value)
        else:
            await self.client.set(key, value)
    
    async def delete(self, key: str):
        """Delete key from Redis."""
        if not self.client:
            await self.connect()
        
        await self.client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self.client:
            await self.connect()
        
        return await self.client.exists(key) > 0


# Global Redis instance
_redis_service = RedisService()


async def get_redis_client() -> RedisService:
    """Get Redis client."""
    if not _redis_service.client:
        await _redis_service.connect()
    return _redis_service
