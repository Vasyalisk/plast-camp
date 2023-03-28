from services.base import BaseService
import schemas.users
from core import security
import models


class Me(BaseService):
    async def get(self, authorize: security.Authorize) -> schemas.users.MeResponse:
        user = await authorize.user_or_401()
        await user.fetch_related("country")
        return schemas.users.MeResponse.from_orm(user)


class Detail(BaseService):
    async def get(self, user_id: int, authorize: security.Authorize) -> schemas.users.DetailResponse:
        await authorize.user_or_401()
        user = await self.user_or_404(user_id)
        return schemas.users.DetailResponse.from_orm(user)

    async def user_or_404(self, user_id: int):
        user = await models.User.get_or_none(id=user_id).select_related(
            "country"
        ).prefetch_related(
            "membership__camp__country"
        )

        if user is None:
            self.raise_404()

        return user


class Filter(BaseService):
    async def get(
            self, query: schemas.users.FilterQuery, authorize: security.Authorize
    ) -> schemas.users.FilterResponse:
        await authorize.user_or_401()
        raise NotImplementedError
