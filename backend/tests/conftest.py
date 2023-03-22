import pytest
import asyncio
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer
from main import app
from conf import settings

BASE_TEST_CLIENT_URL = "http://test"


# Issue with newer Tortoise versions https://github.com/tortoise/tortoise-orm/issues/1110
@pytest.fixture()
def db():
    initializer(["models"], db_url=settings().DB_URL)
    yield
    finalizer()


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def client(db, event_loop):
    async with AsyncClient(app=app, base_url=BASE_TEST_CLIENT_URL) as client:
        yield client
