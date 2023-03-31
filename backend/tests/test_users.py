from datetime import date, timedelta

import pytest
from dateutil.relativedelta import relativedelta

import models
from conf import settings
from core import errors
from tests import factories

ME_URL = "/users/me"
DETAIL_URL = "/users/{user_id}"
FILTER_URL = "/users"
CREATE_URL = "/users"


async def test_me(client):
    user = factories.UserFactory()

    client.authorize(user.id)
    resp = await client.get(ME_URL)
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == user.id


async def test_detail(client):
    me = factories.UserFactory()
    client.authorize(me.id)

    user = factories.UserFactory()

    resp = await client.get(DETAIL_URL.format(user_id=user.id))
    assert resp.status_code == 200


async def test_filter_empty(client):
    users = factories.UserFactory.create_batch(size=3)
    client.authorize(users[0].id)

    resp = await client.get(FILTER_URL)
    assert resp.status_code == 200

    data = resp.json()
    assert data["total_count"] == len(users)
    assert data["total_pages"] == 1

    assert data["page_size"] == settings().DEFAULT_PAGE_SIZE
    assert data["page"] == 1

    assert len(data["results"]) == len(users)


@pytest.mark.parametrize(
    "page,page_size,count,total_count,total_pages", [
        (1, 2, 2, 5, 3),
        (2, 2, 2, 5, 3),
        (3, 2, 1, 5, 3),
        (4, 2, 0, 5, 3),
    ]
)
async def test_filter_pagination(page, page_size, count, total_count, total_pages, client):
    users = factories.UserFactory.create_batch(size=5)
    client.authorize(users[0].id)

    query = {"page": page, "page_size": page_size}
    resp = await client.get(FILTER_URL, params=query)

    assert resp.status_code == 200
    data = resp.json()

    assert data["page"] == page
    assert data["page_size"] == page_size
    assert data["total_count"] == total_count
    assert data["total_pages"] == total_pages
    assert len(data["results"]) == count


async def test_filter_search(client):
    factories.UserFactory.create_batch(size=2, first_name="", last_name="", nickname="")
    factories.UserFactory.create(first_name="test", last_name="", nickname="")
    factories.UserFactory.create(first_name="", last_name="test", nickname="")
    user = factories.UserFactory.create(first_name="", last_name="", nickname="test")

    client.authorize(user.id)
    query = {"search": "eS"}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_count"] == 3
    assert len(data["results"]) == 3


async def test_filter_role(client):
    factories.UserFactory.create_batch(size=2, role=models.User.Role.ADMIN)
    users = factories.BaseUserFactory.create_batch(size=3)

    client.authorize(users[0].id)
    query = {"role": models.User.Role.BASE.value}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_count"] == 3
    assert len(data["results"]) == 3


async def test_filter_camp_role(client):
    factories.UserFactory.create_batch(size=2)
    user1 = factories.UserFactory.create()
    user2 = factories.UserFactory.create()

    factories.CampMemberFactory.create_batch(size=2, user=user1, role=models.CampMember.Role.PARTICIPANT)
    factories.CampMemberFactory.create(user=user2, role=models.CampMember.Role.PARTICIPANT)

    client.authorize(user1.id)
    query = {"camp_role": models.CampMember.Role.PARTICIPANT.value}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["results"]) == 2
    user_ids = {one["id"] for one in data["results"]}
    assert user_ids == {user1.id, user2.id}


async def test_filter_country_id(client):
    factories.UserFactory.create_batch(size=2)
    country = factories.CountryFactory.create()
    users = factories.UserFactory.create_batch(size=3, country=country)

    client.authorize(users[0].id)
    query = {"country_id": country.id}
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["results"]) == len(users)
    user_ids = {one["id"] for one in data["results"]}
    assert user_ids == {one.id for one in users}


@pytest.mark.parametrize("query,count", [
    ({"age": 14}, 3),
    ({"age__gte": 14}, 4),
    ({"age__lte": 13}, 1),
])
async def test_filter_age(query, count, client):
    user_age = 14
    date_of_birth = date.today() - relativedelta(years=user_age)
    user = factories.UserFactory.create(date_of_birth=date_of_birth)
    factories.UserFactory.create(date_of_birth=date_of_birth + timedelta(days=5))
    factories.UserFactory.create(date_of_birth=date_of_birth + timedelta(days=3))

    factories.UserFactory.create(date_of_birth=date_of_birth + relativedelta(years=1))
    factories.UserFactory.create(date_of_birth=date_of_birth - timedelta(days=10))

    client.authorize(user.id)
    resp = await client.get(FILTER_URL, params=query)
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["results"]) == count


async def test_create(client):
    user = factories.SuperAdminUserFactory()
    client.authorize(user.id)

    payload = {}
    resp = await client.post(CREATE_URL, json=payload)
    assert resp.status_code == 201

    data = resp.json()
    user_id = data["id"]
    created = await models.User.get_or_none(id=user_id)
    assert created
    assert created.role == models.User.Role.BASE


async def test_create_permission_denied(client):
    user = factories.UserFactory(role=models.User.Role.ADMIN)
    client.authorize(user.id)

    payload = {"email": "user@test.email"}
    resp = await client.post(CREATE_URL, json=payload)
    assert resp.status_code == 403

    is_created = await models.User.filter(email=payload["email"]).exists()
    assert not is_created


async def test_create_optional_fields(client):
    user = factories.SuperAdminUserFactory()
    country = factories.CountryFactory()
    client.authorize(user.id)

    payload = {
        "email": "user@test.email",
        "first_name": "Bob",
        "last_name": "Dylan",
        "nickname": "Singer",
        "date_of_birth": date.today().isoformat(),
        "role": models.User.Role.ADMIN,
        "country_id": country.id,
    }
    resp = await client.post(CREATE_URL, json=payload)
    assert resp.status_code == 201
    data = resp.json()

    created = await models.User.get_or_none(id=data["id"])
    assert created
    assert created.email == payload["email"]
    assert created.role == payload["role"]


async def test_create_duplicate(client):
    duplicate_email = "user@test.mail"

    factories.UserFactory.create(email=duplicate_email)
    user = factories.SuperAdminUserFactory()
    client.authorize(user.id)

    payload = {"email": duplicate_email}
    resp = await client.post(CREATE_URL, json=payload)
    assert resp.status_code == 400
    data = resp.json()

    assert data["detail"] == errors.DUPLICATE_EMAIL
