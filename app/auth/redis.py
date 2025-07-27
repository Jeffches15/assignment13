# app/auth/redis.py

import redis.asyncio as redis  # ✅ Use redis-py's asyncio support
from app.core.config import get_settings

settings = get_settings()

# Optional: define a connection pool globally if needed
_redis_client = None

async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(settings.REDIS_URL or "redis://localhost")
    return _redis_client

async def add_to_blacklist(jti: str, exp: int):
    """Add a token's JTI to the blacklist"""
    redis_conn = await get_redis()
    await redis_conn.set(f"blacklist:{jti}", "1", ex=exp)

async def is_blacklisted(jti: str) -> bool:
    """Check if a token's JTI is blacklisted"""
    redis_conn = await get_redis()
    return await redis_conn.exists(f"blacklist:{jti}") > 0  # redis-py returns 0 or 1