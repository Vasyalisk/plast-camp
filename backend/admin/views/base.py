import typing as t
from itertools import chain

from fastapi import Request
from starlette_admin import BaseField, BaseModelView, HasMany, HasOne, RequestAction
from tortoise import models
from tortoise.fields.relational import BackwardFKRelation, ManyToManyFieldInstance
from tortoise.models import Model, QuerySet

import translations
from admin.utils import describe_related_fields, extract_fields

SEARCH_OPERATORS = {
    "eq": lambda f, v: models.Q(**{f + "__iexact": v}),
    "neq": lambda f, v: ~models.Q(**{f + "__iexact": v}),
    "lt": lambda f, v: models.Q(**{f + "__lt": v}),
    "gt": lambda f, v: models.Q(**{f + "__gt": v}),
    "le": lambda f, v: models.Q(**{f + "__lte": v}),
    "ge": lambda f, v: models.Q(**{f + "__gte": v}),
    "in": lambda f, v: models.Q(**{f + "__in": v}),
    "not_in": lambda f, v: ~models.Q(**{f + "__in": v}),
    "startswith": lambda f, v: models.Q(**{f + "__istartswith": v}),
    "not_startswith": lambda f, v: ~models.Q(**{f + "__istartswith": v}),
    "endswith": lambda f, v: models.Q(**{f + "__iendswith": v}),
    "not_endswith": lambda f, v: ~models.Q(**{f + "__iendswith": v}),
    "contains": lambda f, v: models.Q(**{f + "__icontains": v}),
    "not_contains": lambda f, v: ~models.Q(**{f + "__icontains": v}),
    "is_false": lambda f, v: models.Q(**{f: False}),
    "is_true": lambda f, v: models.Q(**{f: True}),
    "is_null": lambda f, v: models.Q(**{f + "__isnull": True}),
    "is_not_null": lambda f, v: models.Q(**{f + "__isnull": False}),
    "between": lambda f, v: models.Q(**{f + "__range": v}),
    "not_between": lambda f, v: ~models.Q(**{f + "__range": v}),
}


class TortoiseModelView(BaseModelView):
    model: t.Type[Model] = None
    pk_attr = "id"

    def format_search_string(self, search: str) -> models.Q:
        return models.Q(email=search)

    def format_search_kwarg(self, kwarg, value: t.Union[dict, t.List[dict]]) -> models.Q:
        if kwarg == "and":
            sub_kwargs = []
            for one in value:
                key, val = tuple(one.items())[0]
                sub_kwargs.append(self.format_search_kwarg(key, val))
            return models.Q(*sub_kwargs, join_type=models.Q.AND)

        if kwarg == "or":
            sub_kwargs = []
            for one in value:
                key, val = tuple(one.items())[0]
                sub_kwargs.append(self.format_search_kwarg(key, val))
            return models.Q(*sub_kwargs, join_type=models.Q.OR)

        condition, condition_value = tuple(value.items())[0]
        return SEARCH_OPERATORS[condition](kwarg, condition_value)

    def format_search_filter(self, search: dict) -> t.List[models.Q]:
        kwarg, value = tuple(search.items())[0]
        return [self.format_search_kwarg(kwarg, value)]

    def format_order_by(self, order_by: t.List[str]) -> t.List[str]:
        for field in order_by:
            name, suffix = field.split(" ")
            if suffix == "desc":
                name = f"-{name}"
            yield name

    def get_related_field_names(self) -> t.List[str]:
        names = []
        for field in self.fields:
            if isinstance(field, HasOne):
                names.append(field.name)
            if isinstance(field, HasMany):
                names.append(field.name)
        return names

    def extract_safe_data(self, data: t.Dict[str, t.Any], described_relations: t.Dict[str, dict]) -> t.Dict[str, t.Any]:
        """
        Returns data which is safe to use in model.create() and model.update_from_dict() methods
        :param data:
        :param described_relations:
        :return:
        """
        safe = ((k, v) for k, v in data.items() if k not in described_relations["backward"])
        safe = ((k, v) for k, v in safe if k not in described_relations["many_to_many"])
        safe = dict(safe)
        return safe

    async def load_relations(
            self, data: t.Dict[str, t.Any], described_relations: t.Dict[str, t.Dict[str, dict]]
    ) -> None:
        described_relations_it = chain(
            described_relations["forward"].items(),
            described_relations["backward"].items(),
            described_relations["many_to_many"].items(),
        )

        for related_name, descr in described_relations_it:
            field_type = descr["field_type"]
            has_many = issubclass(field_type, ManyToManyFieldInstance) or issubclass(field_type, BackwardFKRelation)

            if has_many:
                data[related_name] = await descr["python_type"].filter(pk__in=data[related_name])
            else:
                data[related_name] = await descr["python_type"].get_or_none(pk=data[related_name])

    async def update_many_to_many_relations(
            self, model: Model, data: t.Dict[str, t.Any], described_many_to_many_relations: t.Dict[str, dict]
    ):
        for related_name in described_many_to_many_relations:
            m2m_manager = getattr(model, related_name)
            # TODO: update existing models instead of re-creating
            await m2m_manager.clear()
            await m2m_manager.add(data[related_name])

    async def update_backward_relations(
            self, model: Model, data: t.Dict[str, t.Any], described_backward_relations: t.Dict[str, dict]
    ):
        for related_name, descr in described_backward_relations.items():
            related_field = getattr(model, related_name)
            will_delete = not descr["nullable"]
            related_model = related_field.remote_model
            related_fk = related_field.relation_field

            old_relation_pks = await related_field.all().values_list(related_field.from_field, flat=True)
            new_relations = data[related_name]
            new_relation_pks = [one.pk for one in new_relations]

            delete_queryset = related_model.filter(pk__in=set(old_relation_pks).difference(new_relation_pks))
            if will_delete:
                await delete_queryset.delete()
            else:
                await delete_queryset.update(**{related_fk: None})

            await related_model.filter(pk__in=set(new_relation_pks).difference(old_relation_pks)).update(
                **{related_fk: model.pk})

    def get_queryset(self, request: Request) -> QuerySet:
        return self.model.all()

    def get_count_queryset(self, request: Request) -> QuerySet:
        return self.model.all()

    def get_delete_queryset(self, request: Request) -> QuerySet:
        return self.model.all()

    async def count(
            self,
            request: Request,
            where: t.Union[t.Dict[str, t.Any], str, None] = None,
    ) -> int:
        if isinstance(where, str):
            where = self.format_search_string(where)

        if where:
            where = self.format_search_filter(where)

        if where is None:
            where = []

        return await self.get_count_queryset(request).filter(*where).count()

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

        if where:
            where = self.format_search_filter(where)

        if where is None:
            where = []

        if order_by is None:
            order_by = []

        order_by = self.format_order_by(order_by)
        return await self.get_queryset(request).filter(*where).order_by(*order_by).offset(skip).limit(limit)

    async def find_by_pk(self, request: Request, pk: int) -> t.Optional[Model]:
        return await self.get_queryset(request).get_or_none(**{self.pk_attr: pk})

    async def find_by_pks(self, request: Request, pks: t.List[Model]) -> t.Sequence[Model]:
        return await self.get_queryset(request).filter(**{f"{self.pk_attr}__in": pks})

    async def create(self, request: Request, data: dict) -> Model:
        related_field_names = self.get_related_field_names()
        related_field_names = [one for one in related_field_names if one in data]
        descr = describe_related_fields(self.model, related_field_names)
        await self.load_relations(data, descr)

        model = await self.model.create(**self.extract_safe_data(data, descr))

        await self.update_many_to_many_relations(model, data, descr["many_to_many"])
        await self.update_backward_relations(model, data, descr["backward"])
        return model

    async def edit(self, request: Request, pk: int, data: t.Dict[str, t.Any]) -> Model:
        related_field_names = self.get_related_field_names()
        related_field_names = [one for one in related_field_names if one in data]
        descr = describe_related_fields(self.model, related_field_names)
        await self.load_relations(data, descr)

        model = await self.find_by_pk(request, pk)
        model = model.update_from_dict(self.extract_safe_data(data, descr))
        await model.save()

        await self.update_many_to_many_relations(model, data, descr["many_to_many"])
        await self.update_backward_relations(model, data, descr["backward"])
        return model

    async def delete(self, request: Request, pks: t.List[int]) -> t.Optional[int]:
        return await self.get_delete_queryset(request).filter(**{f"{self.pk_attr}__in": pks}).delete()

    def get_fields_list(self, request: Request, action: RequestAction = RequestAction.LIST) -> t.Sequence[BaseField]:
        """
        Returns list of fields to render in form OR list of fields which will be used to update DB model
        :param request:
        :param action:
        :return:
        """
        return extract_fields(request, self.fields, action)

    async def _configs(self, request: Request) -> t.Dict[str, t.Any]:
        conf = await super()._configs(request)
        locale = translations.get_locale()
        conf["locale"] = locale
        conf["dt_i18n_url"] = request.url_for(
            f"{request.app.state.ROUTE_NAME}:statics", path=f"i18n/dt/{locale}.json"
        )
        return conf
