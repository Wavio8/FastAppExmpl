from fastapi import APIRouter, Depends
from app.schemas import SearchRequest, SearchResponse, SearchHit
from app.deps import get_qdrant, get_redis
from app.services.search import search as search_qdrant
from app.services.cache import cache_key, get_cached, set_cached
import redis.asyncio as aioredis
from qdrant_client import QdrantClient

router = APIRouter(tags=["search"])

@router.post("/search", response_model=SearchResponse)
async def search(
    req: SearchRequest,
    qdrant: QdrantClient = Depends(get_qdrant),
    redis: aioredis.Redis = Depends(get_redis),
):
    key = cache_key("search", req.model_dump())
    if req.use_cache:
        cached = await get_cached(redis, key)
        if cached:
            return SearchResponse(hits=[SearchHit(**h) for h in cached])

    hits = search_qdrant(qdrant, req.query, req.top_k)
    await set_cached(redis, key, hits, ttl_sec=120)
    return SearchResponse(hits=[SearchHit(**h) for h in hits])
