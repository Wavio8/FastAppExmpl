from pydantic import BaseModel, Field
from typing import List, Optional

class IndexItem(BaseModel):
    id: str = Field(..., description="Уникальный ID документа")
    text: str = Field(..., description="Текст для индексации")

class IndexRequest(BaseModel):
    items: List[IndexItem]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    use_cache: bool = True

class SearchHit(BaseModel):
    id: str
    score: float
    text: Optional[str] = None

class SearchResponse(BaseModel):
    hits: List[SearchHit]

class HealthResponse(BaseModel):
    status: str
    redis: str
    qdrant: str
