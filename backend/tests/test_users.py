from tests import factories

ME_URL = "/users/me"
DETAIL_URL = "/users/{user_id}"


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
