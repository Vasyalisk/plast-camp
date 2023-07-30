from datetime import date, timedelta

import pytest

import models
import schemas.camps
from tests import factories

DETAIL_URL = "/camps/{camp_id}"
CREATE_URL = "/camps"
DELETE_URL = "/camps/{camp_id}"
FILTER_URL = "/camps"
TODAY = date.today()


@pytest.fixture()
def country_list():
    country1 = factories.CountryFactory(name_ukr="b")
    country2 = factories.CountryFactory(name_ukr="a")
    country3 = factories.CountryFactory(name_ukr="a")
    return [country1, country2, country3]


@pytest.fixture()
def camp_list(country_list):
    camp1 = factories.CampFactory(
        country_id=country_list[0].id,
        date_start=TODAY - timedelta(days=10),
        date_end=TODAY - timedelta(days=7),
        name="First",
        location=""
    )
    camp2 = factories.CampFactory(
        country_id=country_list[0].id,
        date_start=TODAY - timedelta(days=10),
        date_end=TODAY - timedelta(days=5),
        name="Second",
        location="lake"
    )
    camp3 = factories.CampFactory(
        country_id=country_list[1].id,
        date_start=TODAY - timedelta(days=6),
        date_end=TODAY,
        name="Third",
        location="lake"
    )
    return [camp1, camp2, camp3]


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


async def test_filter_empty(client, camp_list):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)
    camp_ids = [one.id for one in camp_list]

    resp = await client.get(FILTER_URL)
    assert resp.status_code == 200

    data = resp.json()
    assert [one["id"] for one in data["results"]] == camp_ids


@pytest.mark.parametrize(
    "order_by,indexes",
    [
        (schemas.camps.FilterOrder.CREATED_AT_ASC.value, range(3)),
        (schemas.camps.FilterOrder.CREATED_AT_DESC.value, range(2, -1, -1)),

        (schemas.camps.FilterOrder.DATE_START_ASC.value, range(3)),
        (schemas.camps.FilterOrder.DATE_START_DESC.value, (2, 0, 1)),

        (schemas.camps.FilterOrder.NAME_ASC.value, range(3)),
        (schemas.camps.FilterOrder.NAME_DESC.value, range(2, -1, -1)),

        (schemas.camps.FilterOrder.COUNTRY_ASC.value, [2, 0, 1]),
        (schemas.camps.FilterOrder.COUNTRY_DESC.value, range(3)),
    ],
)
async def test_filter_order_by(order_by, indexes, client, camp_list):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)
    camp_ids = [camp_list[i].id for i in indexes]

    query = {"order_by": order_by}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert [one["id"] for one in data["results"]] == camp_ids


@pytest.mark.parametrize("country_index,indexes", (
        (0, (0, 1)),
        (1, (2,)),
        (2, ()),
))
async def test_filter_country_id(country_index, indexes, client, camp_list, country_list):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)
    camp_ids = [camp_list[i].id for i in indexes]

    query = {"country_id": country_list[country_index].id}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert [one["id"] for one in data["results"]] == camp_ids


@pytest.mark.parametrize("query,indexes", (
        ({"search": "ir"}, (0, 2)),
        ({"search": "s"}, (0, 1)),
        ({"search": "tHiRd"}, (2,)),
        ({"search": "lake"}, (1, 2)),
        ({"date_from": TODAY - timedelta(days=10)}, range(3)),
        ({"date_from": TODAY - timedelta(days=6)}, (1, 2)),
        ({"date_from": TODAY - timedelta(days=4)}, (2,)),
        ({"date_till": TODAY - timedelta(days=7)}, (0, 1)),
        ({"date_till": TODAY}, range(3)),
        ({"date_from": TODAY - timedelta(days=6), "date_till": TODAY}, (1, 2)),
        ({"date_from": TODAY - timedelta(days=10), "date_till": TODAY - timedelta(days=7)}, (0, 1)),
))
async def test_filter(query, indexes, client, camp_list):
    user = factories.UserFactory(role=models.User.Role.BASE)
    client.authorize(user.id)
    camp_ids = [camp_list[i].id for i in indexes]

    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert [one["id"] for one in data["results"]] == camp_ids

async def test_my_filter():
    # TODO
    pass

async def test_membership():
    # TODO
    pass
