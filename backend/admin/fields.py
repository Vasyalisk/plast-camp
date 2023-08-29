import typing as t
from dataclasses import dataclass

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

    def parse_obj(self, request, obj):
        return obj

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
