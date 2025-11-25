from fastapi import FastAPI
from app.routers import health, index, search,iris
from app.config import settings
import asyncio
import atexit

app = FastAPI(title="FastAPI + Redis + Qdrant Demo", version="0.1.0")

# Routers
app.include_router(health.router)
app.include_router(index.router)
app.include_router(search.router)
app.include_router(iris.router)

# Локальный запуск:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
def close_event_loop():
    try:
        loop = asyncio.get_event_loop()
        if not loop.is_closed():
            loop.close()
    except RuntimeError:
        pass

atexit.register(close_event_loop)