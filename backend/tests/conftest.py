import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from main import app
from conf import settings


@pytest.fixture()
def db():
    initializer(["models"], db_url=settings().DB_URL)
    yield
    finalizer()


# Issue with newer Tortoise versions https://github.com/tortoise/tortoise-orm/issues/1110
@pytest.fixture()
def client(db):
    with TestClient(app) as client:
        yield client
