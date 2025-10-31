import json
import hashlib
from typing import Any
import redis.asyncio as aioredis

def cache_key(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{prefix}:{h}"

async def get_cached(redis: aioredis.Redis, key: str) -> Any | None:
    val = await redis.get(key)
    if not val:
        return None
    return json.loads(val)

async def set_cached(redis: aioredis.Redis, key: str, value: Any, ttl_sec: int = 300) -> None:
    await redis.set(key, json.dumps(value, ensure_ascii=False), ex=ttl_sec)
