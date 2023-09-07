import typing as t
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum

import pytz
from fastapi import Request
from starlette.datastructures import FormData
from starlette_admin import RequestAction, fields
from starlette_admin.helpers import html_params

import translations
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


@dataclass
class DateTimeField(fields.DateTimeField):
    """
    DateTime field which is localized to / from user timezone

    Requires timezone variable to be present in the request session
    """

    async def parse_form_data(
            self, request: Request, form_data: FormData, action: RequestAction
    ) -> t.Any:
        parsed: t.Optional[datetime] = await super().parse_form_data(request, form_data, action)
        if parsed is None:
            return None

        timezone = request.session.get("timezone", "UTC")
        timezone = pytz.timezone(timezone)
        parsed = timezone.localize(parsed).astimezone(pytz.UTC)

        return parsed

    async def serialize_value(
            self, request: Request, value: t.Any, action: RequestAction
    ) -> str:
        assert isinstance(
            value, (datetime, date, time)
        ), f"Expect datetime | date | time, got  {type(value)}"

        if isinstance(value, datetime):
            timezone = request.session.get("timezone", "UTC")
            timezone = pytz.timezone(timezone)
            value = value.astimezone(timezone)

        if action != RequestAction.EDIT:
            return translations.format_datetime(value, self.output_format)

        return value.isoformat()

    def input_params(self) -> str:
        return html_params(
            {
                "type": self.input_type,
                "min": self.min,
                "max": self.max,
                "step": self.step,
                "data_alt_format": self.form_alt_format,
                "data_locale": translations.get_locale(),
                "placeholder": self.placeholder,
                "required": self.required,
                "disabled": self.disabled,
                "readonly": self.read_only,
            }
        )

    def additional_js_links(self, request: Request, action: RequestAction) -> t.List[str]:
        _links = [
            str(
                request.url_for(
                    f"{request.app.state.ROUTE_NAME}:statics",
                    path="js/vendor/flatpickr.min.js",
                )
            )
        ]
        locale = translations.get_locale()
        if locale != "en":
            _links.append(
                str(
                    request.url_for(
                        f"{request.app.state.ROUTE_NAME}:statics",
                        path=f"i18n/flatpickr/{locale}.js",
                    )
                )
            )
        if action.is_form():
            return _links
        return []


@dataclass
class DateField(fields.DateField):
    """
    Date field which is formatted according to current user locale
    """
    async def serialize_value(
            self, request: Request, value: t.Any, action: RequestAction
    ) -> str:
        assert isinstance(value, date), f"Expect date, got  {type(value)}"
        if action != RequestAction.EDIT:
            return translations.format_date(value, self.output_format)
        return value.isoformat()

    def input_params(self) -> str:
        return html_params(
            {
                "type": self.input_type,
                "min": self.min,
                "max": self.max,
                "step": self.step,
                "data_alt_format": self.form_alt_format,
                "data_locale": translations.get_locale(),
                "placeholder": self.placeholder,
                "required": self.required,
                "disabled": self.disabled,
                "readonly": self.read_only,
            }
        )

    def additional_js_links(self, request: Request, action: RequestAction) -> t.List[str]:
        _links = [
            str(
                request.url_for(
                    f"{request.app.state.ROUTE_NAME}:statics",
                    path="js/vendor/flatpickr.min.js",
                )
            )
        ]
        locale = translations.get_locale()
        if locale != "en":
            _links.append(
                str(
                    request.url_for(
                        f"{request.app.state.ROUTE_NAME}:statics",
                        path=f"i18n/flatpickr/{locale}.js",
                    )
                )
            )
        if action.is_form():
            return _links
        return []


@dataclass
class EnumField(fields.EnumField):
    """
    Enum field with custom labels support
    """
    def _get_label(self, value: t.Any, request: Request) -> t.Any:
        if isinstance(value, Enum) and not self.choices and not self.choices_loader:
            return value.name.replace("_", " ")
        for v, label in self._get_choices(request):
            if value == v:
                return label
        raise ValueError(f"Invalid choice value: {value}")
