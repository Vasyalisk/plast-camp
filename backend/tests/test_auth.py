import pytest

from tests import factories
from datetime import date
import models

REGISTER_URL = "/auth/register"


@pytest.mark.asyncio
async def test_register(client):
    payload = {
        "email": "test@user.com",
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]

    user = await models.User.get_or_none(email=payload["email"])
    assert user
    assert user.password != payload["password"]  # type: ignore


def test_register_duplicate(client):
    data = {
        "email": "test@user.com",
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201

    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 400


def test_register_optional_fields(client):
    payload = {
        "email": "test@user.com",
        "password": "abcd",
        "first_name": "John",
        "last_name": "Doe",
        "nickname": "nick",
        "date_of_birth": date.today().isoformat(),
    }
    resp = client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201


def test_register_country(client):
    country = factories.CountryFactory()
    payload = {
        "email": "test@user.com",
        "password": "abcd",
        "country_id": country.id,
    }
    resp = client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201


@pytest.mark.asyncio
async def test_register_existing(client):
    """
    Test user with existing email but missing password is able to register
    :param client:
    :return:
    """
    user = factories.BaseUserFactory(password=None)

    data = {
        "email": user.email,
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201

    await user.refresh_from_db()
    assert user
