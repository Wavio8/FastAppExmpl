from fastapi import APIRouter, Depends
from app.schemas import HealthResponse
from app.deps import get_redis, get_qdrant
import redis.asyncio as aioredis
from qdrant_client import QdrantClient

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health(
    redis: aioredis.Redis = Depends(get_redis),
):
    # Redis
    try:
        pong = await redis.ping()
        redis_status = "ok" if pong else "fail"
    except Exception:
        redis_status = "fail"

    # Qdrant
    try:
        qdrant: QdrantClient = get_qdrant()
        _ = qdrant.get_collections()
        qdrant_status = "ok"
    except Exception:
        qdrant_status = "fail"

    status = "ok" if redis_status == "ok" and qdrant_status == "ok" else "degraded"
    return HealthResponse(status=status, redis=redis_status, qdrant=qdrant_status)
