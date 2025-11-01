from sentence_transformers import SentenceTransformer
from app.config import settings

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """загружает модель при первом вызове"""
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Возвращает эмбеддинги для списка текстов."""
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]


def embed(texts):
    """Обёртка для embed_texts — используется в поисковом сервисе."""
    if isinstance(texts, str):
        texts = [texts]
    model = get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()
