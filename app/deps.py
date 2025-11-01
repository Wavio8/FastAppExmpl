from typing import AsyncGenerator
import redis.asyncio as aioredis
from qdrant_client import QdrantClient
from app.config import settings

# Redis (async)
redis_client: aioredis.Redis | None = None


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    Асинхронный генератор, создающий и корректно закрывающий Redis-клиент.
    """
    global redis_client
    if redis_client is None:
        redis_client = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=getattr(settings, "redis_db", 0),
            decode_responses=True
        )
    try:
        yield redis_client
    finally:
        try:
            await redis_client.aclose()
        except Exception:
            pass


qdrant_client: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    global qdrant_client
    if qdrant_client is None:
        qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
    return qdrant_client
