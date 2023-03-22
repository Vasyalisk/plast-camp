import pytest
from unittest.mock import patch

from tests import factories
from datetime import date
import models
from core import security, redis

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"

MOCKED_USER_CODE = "abcd"


@patch("core.redis.secrets.token_urlsafe", return_value=MOCKED_USER_CODE)
async def test_register(redis_code_mock, client):
    payload = {
        "email": "test@user.com",
        "password": "1234abcd!",
    }
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]

    user = await models.User.get_or_none(email=payload["email"])
    assert user
    assert user.password != payload["password"]  # type: ignore

    redis_user_id = await redis.check_code(MOCKED_USER_CODE, redis.CodeType.REGISTER)
    assert str(user.id) == redis_user_id


async def test_register_duplicate(client):
    data = {
        "email": "test@user.com",
        "password": "1234abcd!",
    }
    resp = await client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201

    resp = await client.post(REGISTER_URL, json=data)
    assert resp.status_code == 400


async def test_register_optional_fields(client):
    payload = {
        "email": "test@user.com",
        "password": "1234abcd!",
        "first_name": "John",
        "last_name": "Doe",
        "nickname": "nick",
        "date_of_birth": date.today().isoformat(),
    }
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201


async def test_register_country(client):
    country = factories.CountryFactory()
    payload = {
        "email": "test@user.com",
        "password": "1234abcd!",
        "country_id": country.id,
    }
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201


async def test_register_existing(client):
    """
    Test user with existing email but missing password is able to register
    :param client:
    :return:
    """
    user = factories.BaseUserFactory(password=None)

    payload = {
        "email": user.email,
        "password": "1234abcd!",
    }
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201

    await user.refresh_from_db()
    assert user


@pytest.mark.parametrize("fields", [
    {"email": "abcd"},
    {"country_id": 1},
    {"password": "abcd"},
])
async def test_register_invalid_fields(fields, client):
    payload = {
        "email": "test@user.com",
        "password": "1234abcd!",
    }
    payload.update(fields)
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code != 201


async def test_login(client):
    password = "abcd1234!"
    user = factories.UserFactory(password=security.hash_password(password))

    payload = {
        "email": user.email,
        "password": password,
    }
    resp = await client.post(LOGIN_URL, json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]
