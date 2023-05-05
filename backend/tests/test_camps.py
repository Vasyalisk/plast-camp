from datetime import date, timedelta

import pytest

import models
from tests import factories

DETAIL_URL = "/camps/{camp_id}"
CREATE_URL = "/camps"
DELETE_URL = "/camps/{camp_id}"


@pytest.mark.parametrize("overrides", [
    {},
    {"country_id": None, "date_start": None, "date_end": None},
])
async def test_detail(client, overrides):
    user = factories.UserFactory()
    client.authorize(user.id)

    camp = factories.CampFactory(**overrides)
    factories.CampFactory()

    resp = await client.get(DETAIL_URL.format(camp_id=camp.id))
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == camp.id


async def test_create(client):
    user = factories.UserFactory(role=models.User.Role.ADMIN)
    client.authorize(user.id)

    body = {"description": "", "location": "", "name": "test"}
    resp = await client.post(CREATE_URL, json=body)
    assert resp.status_code == 201

    data = resp.json()
    camp_id = data["id"]

    camp = await models.Camp.get_or_none(id=camp_id)
    assert camp


async def test_create_optionals(client):
    user = factories.UserFactory(role=models.User.Role.ADMIN)
    client.authorize(user.id)

    country = factories.CountryFactory()

    body = {
        "date_start": (date.today() - timedelta(days=1)).isoformat(),
        "date_end": date.today().isoformat(),

        "description": "test",
        "location": "test",
        "name": "test",

        "country_id": country.id,
    }

    resp = await client.post(CREATE_URL, json=body)
    assert resp.status_code == 201

    data = resp.json()
    camp_id = data["id"]

    camp = await models.Camp.get_or_none(id=camp_id)
    assert camp


async def test_create_permission_denied(client):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)

    body = {"description": "", "location": "", "name": "test"}
    resp = await client.post(CREATE_URL, json=body)
    assert resp.status_code == 403


async def test_delete(client):
    user = factories.UserFactory(role=models.User.Role.ADMIN)
    client.authorize(user.id)

    camp = factories.CampFactory()

    resp = await client.delete(DELETE_URL.format(camp_id=camp.id))
    assert resp.status_code == 204

    camp_exists = await models.Camp.exists(id=camp.id)
    assert not camp_exists


async def test_delete_permission_denied(client):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)

    camp = factories.CampFactory()

    resp = await client.delete(DELETE_URL.format(camp_id=camp.id))
    assert resp.status_code == 403

    camp_exists = await models.Camp.exists(id=camp.id)
    assert camp_exists

async def test_filter():
    # TODO: test filter API
    pass
