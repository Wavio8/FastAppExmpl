from fastapi import FastAPI
from app.routers import health, index, search
from app.config import settings

app = FastAPI(title="FastAPI + Redis + Qdrant Demo", version="0.1.0")

# Routers
app.include_router(health.router)
app.include_router(index.router)
app.include_router(search.router)

# Локальный запуск:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
