from tests import factories

REGISTER_URL = "/auth/register"


def test_register(client):
    data = {
        "email": "test@user.com",
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201

    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]


def test_register_duplicate(client):
    data = {
        "email": "test@user.com",
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201

    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 400


def test_register_existing(client):
    user = factories.BaseUserFactory(password=None)

    data = {
        "email": user.email,
        "password": "abcd",
    }
    resp = client.post(REGISTER_URL, json=data)
    assert resp.status_code == 201
