import typing as t
from datetime import date

import models
import schemas.camps
from core import errors, security
from services import utils
from services.base import BaseService


class Detail(BaseService):
    async def get(self, camp_id: int, authorize: security.Authorize) -> schemas.camps.DetailResponse:
        await authorize.user_or_401()

        camp = await models.Camp.get_or_none(id=camp_id).select_related("country")
        if camp is None:
            raise self.HttpException404()

        return schemas.camps.DetailResponse.from_orm(camp)


class Create(BaseService):
    async def post(self, body: schemas.camps.CreateBody, authorize: security.Authorize) -> schemas.camps.DetailResponse:
        user = await authorize.user_or_401()

        can_create = user.role in (models.User.Role.ADMIN, models.User.Role.SUPER_ADMIN)
        if not can_create:
            raise self.HttpException403()

        await self.validate_country(body.country_id)

        camp = await models.Camp.create(**body.dict(exclude_none=True))
        await camp.fetch_related("country")

        return schemas.camps.DetailResponse.from_orm(camp)

    async def validate_country(self, country_id: t.Optional[int]):
        if country_id is None:
            return

        country_exists = await models.Country.exists(id=country_id)
        if not country_exists:
            raise self.HttpException400(errors.INVALID_COUNTRY_ID)


class Delete(BaseService):
    async def delete(self, camp_id: int, authorize: security.Authorize) -> None:
        user = await authorize.user_or_401()

        can_delete = user.role in (models.User.Role.ADMIN, models.User.Role.SUPER_ADMIN)
        if not can_delete:
            raise self.HttpException403()

        deleted_count = await models.Camp.filter(id=camp_id).delete()
        if not deleted_count:
            raise self.HttpException404()


class Filter(BaseService):
    async def get(
            self,
            order_by: list[schemas.camps.FilterOrder],
            query: schemas.camps.FilterQuery,
            authorize: security.Authorize
    ) -> schemas.camps.FilterResponse:
        await authorize.user_or_401()

        if query.country_id:
            await self.validate_country_id(query.country_id)

        formatted_filters = {"search", "date_from", "date_till"}
        filter_kwargs = query.query_fields(exclude_unset=True, exclude_none=True, exclude=formatted_filters)
        queryset = models.Camp.filter(**filter_kwargs).select_related("country")

        if query.search:
            queryset = queryset.filter(self.format_search_filter(query.search))

        if query.date_from or query.date_till:
            queryset = queryset.filter(self.format_date_range_filter(query.date_from, query.date_till))

        queryset = queryset.order_by(*self.format_order(order_by))
        queryset = utils.paginate_queryset(queryset, query)

        return await utils.paginate_response(queryset, query, schemas.camps.FilterResponse)

    async def validate_country_id(self, country_id):
        exists = await models.Country.exists(id=country_id)
        if not exists:
            raise self.HttpException400(errors.INVALID_COUNTRY_ID)

    def format_search_filter(self, search: str) -> models.Q:
        return models.Q(location__icontains=search, name__icontains=search, join_type=models.Q.OR)

    def format_date_range_filter(self, date_from: t.Optional[date], date_till: t.Optional[date]) -> models.Q:
        date_from = date_from or date.min
        date_till = date_till or date.max

        # Whether date_start is within range [date_from, date_till]
        date_start_overlaps = models.Q(date_start__gte=date_from, date_start__lte=date_till)

        # Whether date_end is within range [date_from, date_till]
        date_end_overlaps = models.Q(date_end__gte=date_from, date_end__lte=date_till)

        # Whether [date_start, date_end] is a sub-range of [date_from, date_till]
        date_range_overlaps = models.Q(date_start__lte=date_from, date_end__gte=date_till, join_type=models.Q.AND)
        return models.Q(date_start_overlaps, date_end_overlaps, date_range_overlaps, join_type=models.Q.OR)

    def format_order(self, order_by: list[schemas.camps.FilterOrder]) -> list[str]:
        # noinspection PyPep8Naming
        Order = schemas.camps.FilterOrder

        order_map = {
            Order.CREATED_AT_ASC: "created_at",
            Order.CREATED_AT_DESC: "-created_at",

            Order.DATE_START_ASC: "date_start",
            Order.DATE_START_DESC: "-date_start",

            Order.COUNTRY_ASC: "country__name_ukr",
            Order.COUNTRY_DESC: "-country__name_ukr",

            Order.NAME_ASC: "name",
            Order.NAME_DESC: "-name",
        }
        return [order_map[one] for one in order_by]
