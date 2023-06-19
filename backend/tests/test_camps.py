from datetime import date, timedelta

import pytest

import models
import schemas.camps
from tests import factories

DETAIL_URL = "/camps/{camp_id}"
CREATE_URL = "/camps"
DELETE_URL = "/camps/{camp_id}"
FILTER_URL = "/camps"


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


async def test_filter_empty(client):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)

    camps = factories.CampFactory.create_batch(size=3)

    resp = await client.get(FILTER_URL)
    assert resp.status_code == 200

    data = resp.json()
    camp_ids = [one["id"] for one in data["results"]]
    assert camp_ids == [one.id for one in camps]


@pytest.mark.parametrize(
    "order_by,db_order",
    [
        (schemas.camps.FilterOrder.CREATED_AT_ASC.value, "created_at"),
        (schemas.camps.FilterOrder.CREATED_AT_DESC.value, "-created_at"),

        (schemas.camps.FilterOrder.DATE_START_ASC.value, "date_start"),
        (schemas.camps.FilterOrder.DATE_START_DESC.value, "-date_start"),

        (schemas.camps.FilterOrder.NAME_ASC.value, "name"),
        (schemas.camps.FilterOrder.NAME_DESC.value, "-name"),

        (schemas.camps.FilterOrder.COUNTRY_ASC.value, "country__name_ukr"),
        (schemas.camps.FilterOrder.COUNTRY_DESC.value, "-country__name_ukr"),
    ],
)
async def test_filter_order_by(order_by, db_order, client):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)

    # Create with different created_at value
    factories.CampFactory()
    factories.CampFactory()
    factories.CampFactory()

    camp_ids = models.Camp.all().order_by(db_order).values_list("id", flat=True)

    query = {"order_by": order_by}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert [one["id"] for one in data["results"]] == camp_ids

async def test_filter():
    # TODO: test filter API by resp of params
    pass
