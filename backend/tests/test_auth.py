from datetime import date
from unittest.mock import patch

import pytest

import models
from core import redis, security
from tests import factories

REGISTER_URL = "/auth/register"
CONFIRM_REGISTRATION_URL = "/auth/register/confirm"
LOGIN_URL = "/auth/login"
CHANGE_PASSWORD_URL = "/auth/password/change"
FORGOT_PASSWORD_URL = "/auth/password/reset/request"
RESET_PASSWORD_URL = "/auth/password/reset"

MOCKED_USER_CODE = "abcd"


@patch("core.redis.secrets.token_urlsafe", return_value=MOCKED_USER_CODE)
async def test_register(redis_code_mock, client, redis_cleanup):
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


async def test_register_duplicate(client, redis_cleanup):
    user = factories.UserFactory()
    data = {
        "email": user.email,
        "password": "1234abcd!",
    }

    resp = await client.post(REGISTER_URL, json=data)
    assert resp.status_code == 400


async def test_register_update_password(client, redis_cleanup):
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


async def test_register_optional_fields(client, redis_cleanup):
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


async def test_register_country(client, redis_cleanup):
    country = factories.CountryFactory()
    payload = {
        "email": "test@user.com",
        "password": "1234abcd!",
        "country_id": country.id,
    }
    resp = await client.post(REGISTER_URL, json=payload)
    assert resp.status_code == 201


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


async def test_confirm_registration(client, redis_cleanup):
    user = factories.UserFactory(is_email_verified=False)
    code = await redis.generate_code(user.id, redis.CodeType.REGISTER)

    payload = {"code": code}
    resp = await client.patch(CONFIRM_REGISTRATION_URL, json=payload)
    assert resp.status_code == 204

    await user.refresh_from_db()
    assert user.is_email_verified == True


async def test_confirm_registration_invalid_code(client):
    payload = {"code": "abcd"}
    resp = await client.patch(CONFIRM_REGISTRATION_URL, json=payload)
    assert resp.status_code == 400


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


@pytest.mark.parametrize("fields", [
    {"email": "invalid@email.com"},
    {"password": "invalid"},
])
async def test_login_invalid(fields, client):
    email = "test@user.com"
    password = "1234Abcd!"
    factories.UserFactory(password=security.hash_password(password), email=email)

    payload = {
        "email": email,
        "password": password,
    }
    payload.update(fields)
    resp = await client.post(LOGIN_URL, json=payload)
    assert resp.status_code == 401


async def test_change_password(client):
    password = "1234Abcd!"
    user = factories.UserFactory(password=security.hash_password(password))
    client.authorize(user.id)

    payload = {
        "new_password": "5678Abcd!",
        "old_password": password
    }
    resp = await client.patch(CHANGE_PASSWORD_URL, json=payload)
    assert resp.status_code == 204


@pytest.mark.parametrize("fields", [
    {"new_password": "123"},
    {"old_password": "123"},
])
async def test_change_password_invalid(fields, client):
    password = "1234Abcd!"
    user = factories.UserFactory(password=security.hash_password(password))
    client.authorize(user.id)

    payload = {
        "new_password": "4567Abcd!",
        "old_password": password,
    }
    payload.update(fields)
    resp = await client.patch(CHANGE_PASSWORD_URL, json=payload)
    assert 500 > resp.status_code >= 400


async def test_change_password_unauthorized(client):
    payload = {
        "new_password": "4567Abcd!",
        "old_password": "1234Abcd",
    }
    resp = await client.patch(CHANGE_PASSWORD_URL, json=payload)
    assert resp.status_code == 401


@patch("core.redis.secrets.token_urlsafe", return_value=MOCKED_USER_CODE)
async def test_forgot_password(redis_code_mock, client, redis_cleanup):
    user = factories.UserFactory()
    payload = {"email": user.email}

    resp = await client.post(FORGOT_PASSWORD_URL, json=payload)
    assert resp.status_code == 204

    is_code_created = await redis.check_code(MOCKED_USER_CODE, redis.CodeType.FORGOT_PASSWORD)
    assert is_code_created


@patch("core.redis.secrets.token_urlsafe", return_value=MOCKED_USER_CODE)
async def test_forgot_password_invalid_email(redis_code_mock, client, redis_cleanup):
    payload = {"email": "test@email.com"}

    resp = await client.post(FORGOT_PASSWORD_URL, json=payload)
    assert resp.status_code == 204

    is_code_created = await redis.check_code(MOCKED_USER_CODE, redis.CodeType.FORGOT_PASSWORD)
    assert not is_code_created


async def test_reset_password(client, redis_cleanup):
    user = factories.UserFactory()
    code = await redis.generate_code(user.id, redis.CodeType.FORGOT_PASSWORD)

    new_password = "1234Abcd!"
    payload = {"code": code, "password": new_password}
    resp = await client.post(RESET_PASSWORD_URL, json=payload)
    assert resp.status_code == 204

    await user.refresh_from_db()
    assert security.verify_password(new_password, user.password)


@pytest.mark.parametrize("fields", [
    {"code": "invalid"},
    {"password": "123"},
])
@patch("core.redis.secrets.token_urlsafe", return_value=MOCKED_USER_CODE)
async def test_reset_password_invalid(redis_code_mock, fields, client, redis_cleanup):
    user = factories.UserFactory()
    await redis.generate_code(user.id, redis.CodeType.FORGOT_PASSWORD)

    payload = {"code": MOCKED_USER_CODE, "password": "1234Abcd!"}
    payload.update(fields)
    resp = await client.post(RESET_PASSWORD_URL, json=payload)
    assert 500 > resp.status_code >= 400
