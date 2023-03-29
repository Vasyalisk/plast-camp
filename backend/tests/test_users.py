import pytest

import models
from tests import factories
from conf import settings

ME_URL = "/users/me"
DETAIL_URL = "/users/{user_id}"
FILTER_URL = "/users"


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
    membership = factories.CampMemberFactory.create_batch(size=3, user=user)

    resp = await client.get(DETAIL_URL.format(user_id=user.id))
    assert resp.status_code == 200

    data = resp.json()
    assert len(data["membership"]) == len(membership)


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
    assert False


async def test_filter_country_id(client):
    assert False


async def test_filter_age(client):
    assert False


async def test_filter_age_range(client):
    assert False
