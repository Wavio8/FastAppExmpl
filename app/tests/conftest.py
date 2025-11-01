import os
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def test_env():
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")
    os.environ.setdefault("QDRANT_HOST", "localhost")
    os.environ.setdefault("QDRANT_PORT", "6333")
    os.environ.setdefault("QDRANT_COLLECTION", "test_docs")
    yield


@pytest.fixture(scope="function")
def client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TestClient(app) as c:
        yield c
    loop.close()
