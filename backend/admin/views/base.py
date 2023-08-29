import typing as t

from fastapi import Request
from starlette_admin import BaseField, BaseModelView, RequestAction
from tortoise.models import Model

from admin.utils import extract_fields


class TortoiseModelView(BaseModelView):
    model: Model = None
    pk_attr = "id"

    def format_search_string(self, search: str) -> t.Dict[str, t.Any]:
        return {"email": search}

    def format_order_by(self, order_by: t.List[str]) -> t.List[str]:
        for field in order_by:
            name, suffix = field.split(" ")
            if suffix == "desc":
                name = f"-{name}"
            yield name

    async def count(
            self,
            request: Request,
            where: t.Union[t.Dict[str, t.Any], str, None] = None,
    ) -> int:
        if isinstance(where, str):
            where = self.format_search_string(where)

        if where is None:
            where = {}

        return await self.model.filter(**where).count()

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 50,
            where: t.Union[t.Dict[str, t.Any], str, None] = None,
            order_by: t.Optional[t.List[str]] = None,
    ) -> t.Sequence[t.Any]:
        if isinstance(where, str):
            where = self.format_search_string(where)

        if where is None:
            where = {}

        if order_by is None:
            order_by = []

        order_by = self.format_order_by(order_by)
        return await self.model.filter(**where).order_by(*order_by).offset(skip).limit(limit)

    async def find_by_pk(self, request: Request, pk: int) -> t.Optional[Model]:
        return await self.model.get_or_none(**{self.pk_attr: pk})

    async def find_by_pks(self, request: Request, pks: t.List[Model]) -> t.Sequence[Model]:
        return await self.model.filter(**{f"{self.pk_attr}__in": pks})

    async def create(self, request: Request, data: dict) -> Model:
        return await self.model.create(**data)

    async def edit(self, request: Request, pk: int, data: t.Dict[str, t.Any]) -> Model:
        model = await self.find_by_pk(request, pk)
        model = model.update_from_dict(data)
        await model.save()
        return model

    async def delete(self, request: Request, pks: t.List[int]) -> t.Optional[int]:
        return await self.model.filter(**{f"{self.pk_attr}__in": pks}).delete()

    def get_fields_list(self, request: Request, action: RequestAction = RequestAction.LIST) -> t.Sequence[BaseField]:
        """
        Returns list of fields to render in form OR list of fields which will be used to update DB model
        :param request:
        :param action:
        :return:
        """
        return extract_fields(request, self.fields, action)
