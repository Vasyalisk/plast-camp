import typing as t
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

import models
import schemas.users
from core import errors, security
from services import utils
from services.base import BaseService


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
        user = await models.User.get_or_none(id=user_id).select_related("country")

        if user is None:
            self.raise_404()

        return user


class Filter(BaseService):
    async def get(
            self, query: schemas.users.FilterQuery, authorize: security.Authorize
    ) -> schemas.users.FilterResponse:
        await self.validate(query, authorize)

        formatted_filters = {"search", "membership__role", "age", "age__gte", "age__lte"}
        filter_kwargs = query.query_fields(exclude_unset=True, exclude_none=True, exclude=formatted_filters)
        queryset = models.User.filter(**filter_kwargs).select_related("country")

        if query.membership__role:
            queryset = queryset.filter(self.format_membership__role_filter(query.membership__role))

        if query.search:
            queryset = queryset.filter(self.format_search_filter(query.search))

        if query.age:
            queryset = queryset.filter(self.format_age_filter(query.age))

        if query.age__gte or query.age__lte:
            queryset = queryset.filter(self.format_age_range_filter(age__gte=query.age__gte, age__lte=query.age__lte))

        return await utils.paginate_response(queryset, request_query=query, response_model=schemas.users.FilterResponse)

    async def validate(self, query: schemas.users.FilterQuery, authorize: security.Authorize):
        await authorize.user_or_401()

        if query.country_id is not None:
            await self.validate_country_id(query.country_id)

    async def validate_country_id(self, country_id: int):
        is_valid = await models.Country.filter(id=country_id).exists()

        if not is_valid:
            self.raise_400(errors.INVALID_COUNTRY_ID)

    def format_age_filter(self, age: int) -> models.Q:
        dob_min = date.today() - relativedelta(years=age)
        dob_max = dob_min + relativedelta(years=1) - timedelta(days=1)
        return models.Q(date_of_birth__gte=dob_min, date_of_birth__lte=dob_max)

    def format_age_range_filter(self, age__gte: t.Optional[int], age__lte: t.Optional[int]):
        kwargs = {}

        if age__gte:
            dob_min = date.today() - relativedelta(years=age__gte)
            kwargs["date_of_birth__gte"] = dob_min

        if age__lte:
            dob_max = date.today() - relativedelta(years=age__lte + 1) - timedelta(days=1)
            kwargs["date_of_birth__lte"] = dob_max

        return models.Q(**kwargs)

    def format_membership__role_filter(self, role: t.Union[models.CampMember.Role, str]) -> models.Q:
        user_id_subquery = models.CampMember.filter(role=role).group_by("user_id").values("user_id")
        return models.Q(id__in=models.Subquery(user_id_subquery))

    def format_search_filter(self, search: str) -> models.Q:
        return models.Q(
            first_name__icontains=search,
            last_name__icontains=search,
            nickname__icontains=search,
            join_type=models.Q.OR,
        )


class Create(BaseService):
    async def post(self, body: schemas.users.CreateBody, authorize: security.Authorize) -> schemas.users.CreateResponse:
        creator = await authorize.user_or_401()
        await self.validate_permission(creator)

        if body.email:
            await self.validate_email(body.email)

        if body.country_id:
            await self.validate_country_id(body.country_id)

        payload = body.dict()
        user = await models.User.create(**payload)
        await user.fetch_related("country")

        return schemas.users.CreateResponse.from_orm(user)

    async def validate_email(self, email: str):
        exists = await models.User.filter(email=email).exists()

        if exists:
            self.raise_400(errors.DUPLICATE_EMAIL)

    async def validate_country_id(self, country_id: int):
        is_valid = await models.Country.filter(id=country_id).exists()

        if not is_valid:
            self.raise_400(errors.INVALID_COUNTRY_ID)

    async def validate_permission(self, user: models.User):
        if user.role != models.User.Role.SUPER_ADMIN:
            self.raise_403()
