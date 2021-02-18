from typing import List
import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient


@pytest.fixture(scope="session")
def app():
    from src.api.server import app
    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
        ) as client:
            yield client
