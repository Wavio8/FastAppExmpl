from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from typing import Iterable
from app.config import settings
from app.services.embeddings import embed_texts

def ensure_collection(client: QdrantClient, vector_size: int):
    collections = client.get_collections().collections
    names = {c.name for c in collections}
    if settings.qdrant_collection not in names:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def index_items(client: QdrantClient, items: list[dict]):
    texts = [it["text"] for it in items]
    ids = [it["id"] for it in items]
    vectors = embed_texts(texts)
    ensure_collection(client, vector_size=len(vectors[0]))
    points: Iterable[PointStruct] = (
        PointStruct(id=ids[i], vector=vectors[i], payload={"text": texts[i]})
        for i in range(len(ids))
    )
    client.upsert(collection_name=settings.qdrant_collection, points=points)

def search(client: QdrantClient, query: str, top_k: int = 5) -> list[dict]:
    vec = embed_texts([query])[0]
    ensure_collection(client, vector_size=len(vec))
    res = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=vec,
        limit=top_k,
        with_payload=True
    )
    hits = []
    for r in res:
        hits.append({
            "id": str(r.id),
            "score": float(r.score),
            "text": r.payload.get("text") if r.payload else None
        })
    return hits
