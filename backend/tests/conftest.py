import pytest
import asyncio
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer
from main import app
from conf import settings
from core import security, redis

BASE_TEST_CLIENT_URL = "http://test"


class TestClient(AsyncClient):
    def authorize(self, user_id):
        token = security.Authorize().create_access_token(user_id)
        self.headers["Authorization"] = f"Bearer {token}"

    # noinspection SpellCheckingInspection
    def unauthorize(self):
        self.headers.pop("Authorization", None)

    @property
    def is_authorized(self) -> bool:
        return "Authorization" in self.headers


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
async def redis_cleanup(event_loop):
    yield
    await redis.connection.flushdb()


@pytest.fixture()
async def client(db, event_loop):
    async with TestClient(app=app, base_url=BASE_TEST_CLIENT_URL) as client:
        yield client
