from services.base import BaseService
from services import utils
import schemas.users
from core import security, errors
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
        await self.validate(query, authorize)

        filter_kwargs = query.query_fields(exclude_unset=True, exclude_none=True, exclude={"search"})
        queryset = models.User.all().select_related("country").prefetch_related("membership__camp__country")
        queryset = queryset.filter(**filter_kwargs)

        if query.search:
            queryset = queryset.filter(self.format_search_filter(query.search))

        return await utils.paginate_response(queryset, request_query=query, response_model=schemas.users.FilterResponse)

    async def validate(self, query: schemas.users.FilterQuery, authorize: security.Authorize):
        await authorize.user_or_401()

        if query.country_id is not None:
            await self.validate_country_id(query.country_id)

    async def validate_country_id(self, country_id: int):
        is_valid = await models.Country.filter(id=country_id).exists()

        if not is_valid:
            self.raise_400(errors.INVALID_COUNTRY_ID)

    def format_search_filter(self, search: str) -> models.Q:
        return models.Q(
            first_name__icontains=search,
            last_name__icontains=search,
            nickname__icontains=search,
            join_type=models.Q.OR,
        )
