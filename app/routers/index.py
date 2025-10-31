from fastapi import APIRouter, Depends
from app.schemas import IndexRequest
from app.deps import get_qdrant
from app.services.search import index_items
from qdrant_client import QdrantClient

router = APIRouter(tags=["indexing"])

@router.post("/index")
def index(req: IndexRequest, qdrant: QdrantClient = Depends(get_qdrant)):
    items = [it.model_dump() for it in req.items]
    index_items(qdrant, items)
    return {"status": "ok", "indexed": len(items)}
