from fastapi import APIRouter, Depends
from app.schemas import ItemList
from app.services.search import index_items
from app.deps import get_qdrant

router = APIRouter()

@router.post("/index")
def index(request: ItemList, qdrant=Depends(get_qdrant)):
    count = index_items(qdrant, request.items)
    return {"status": "ok", "indexed": count}