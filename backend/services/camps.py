from services.base import BaseService
import schemas.camps
from core import security, errors
import models
import typing as t


class Detail(BaseService):
    async def get(self, camp_id: int, authorize: security.Authorize) -> schemas.camps.DetailResponse:
        await authorize.user_or_401()

        camp = await models.Camp.get_or_none(id=camp_id).select_related("country")
        if camp is None:
            self.raise_404()

        return schemas.camps.DetailResponse.from_orm(camp)


class Create(BaseService):
    async def post(self, body: schemas.camps.CreateBody, authorize: security.Authorize) -> schemas.camps.DetailResponse:
        user = await authorize.user_or_401()

        can_create = user.role in (models.User.Role.ADMIN, models.User.Role.SUPER_ADMIN)
        if not can_create:
            self.raise_403()

        await self.validate_country(body.country_id)

        camp = await models.Camp.create(**body.dict(exclude_none=True))
        await camp.fetch_related("country")
        
        return schemas.camps.DetailResponse.from_orm(camp)

    async def validate_country(self, country_id: t.Optional[int]):
        if country_id is None:
            return

        country_exists = await models.Country.exists(id=country_id)
        if not country_exists:
            self.raise_400(errors.INVALID_COUNTRY_ID)
