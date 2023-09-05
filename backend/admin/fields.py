import typing as t
from dataclasses import dataclass
from datetime import datetime

import pytz
from fastapi import Request
from starlette.datastructures import FormData
from starlette_admin import RequestAction, fields

from admin.utils import extract_fields


@dataclass(init=False)
class ContainerField(fields.CollectionField):
    """
    Field to group other fields under same section in the detail view
    """
    exclude_from_list = True
    is_container = True

    def __init__(self, name: str, fields: t.Sequence[fields.BaseField], label=None, required: bool = False):
        self.label = label
        super().__init__(name, fields, required)

    def parse_obj(self, request, obj):
        return obj

    # TODO: fix nested HasOne / HasMany / Enum fields
    async def parse_form_data(self, request: Request, form_data: FormData, action: RequestAction) -> t.Any:
        data = {}
        for field in self.get_fields_list(request, action):
            data[field.name] = await field.parse_form_data(request, form_data, action)
        return data

    def get_fields_list(
            self,
            request: Request,
            action: RequestAction = RequestAction.LIST,
    ) -> t.Sequence[fields.BaseField]:
        return extract_fields(request, self.fields, action)

    # async def serialize_value(
    #         self, request: Request, value: t.Any, action: RequestAction
    # ) -> t.Any:
    #     data = {}
    #
    #     for field in self.get_fields_list(request, action):
    #         if hasattr(value, field.name):
    #             field_value = getattr(value, field.name)
    #         else:
    #             field_value = value[field.name]
    #
    #         if field_value is None:
    #             data[field.name] = await field.serialize_none_value(request, action)
    #         else:
    #             data[field.name] = await field.serialize_value(request, field_value, action)
    #     return data


@dataclass
class AwareDateTimeField(fields.DateTimeField):
    """
    DateTime field which is localized to / from user timezone.
    Requires timezone variable to be present in the request session
    """

    async def parse_form_data(
            self, request: Request, form_data: FormData, action: RequestAction
    ) -> t.Any:
        parsed: t.Optional[datetime] = await super().parse_form_data(request, form_data, action)
        timezone = request.session.get("timezone", "UTC")
        timezone = pytz.timezone(timezone)
        parsed = timezone.localize(parsed).astimezone(pytz.UTC)

        return parsed

    async def serialize_value(
            self, request: Request, value: t.Any, action: RequestAction
    ) -> str:
        if isinstance(value, datetime):
            timezone = request.session.get("timezone", "UTC")
            timezone = pytz.timezone(timezone)
            value = value.astimezone(timezone)

        return await super().serialize_value(request, value, action)
