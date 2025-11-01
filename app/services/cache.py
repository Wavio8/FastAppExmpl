import json
import hashlib
from typing import Any, AsyncGenerator
import redis.asyncio as aioredis


# ключи кэша
def cache_key(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{prefix}:{h}"


# создание / закрытие Redis-клиента
async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Асинхронный контекстный менеджер для работы с Redis"""
    redis = aioredis.from_url(
        "redis://localhost",
        decode_responses=True,
        encoding="utf-8"
    )
    try:
        yield redis
    finally:
        try:
            await redis.close()
        except Exception:
            pass


async def get_cached(redis: aioredis.Redis, key: str) -> Any | None:
    """Получение значения из Redis"""
    val = await redis.get(key)
    if not val:
        return None
    return json.loads(val)


async def set_cached(redis: aioredis.Redis, key: str, value: Any, ttl_sec: int = 300) -> None:
    """Сохранение значения в Redis с TTL"""
    await redis.set(key, json.dumps(value, ensure_ascii=False), ex=ttl_sec)
