import typing as t

from fastapi import Request
from starlette_admin import BaseField, RequestAction


def extract_fields(
        request: Request,
        fields: t.Sequence["BaseField"],
        action: RequestAction = RequestAction.LIST,
) -> t.Sequence["BaseField"]:
    """Extract fields based on the requested action and exclude flags."""
    arr = []
    for field in fields:
        # Ignore non-editable fields when updating DB model
        if request.method.lower() != "get" and any((
                field.read_only,
                field.disabled,
        )):
            continue

        # Exclude fields from respective views
        if any((
                action == RequestAction.LIST and field.exclude_from_list,
                action == RequestAction.DETAIL and field.exclude_from_detail,
                action == RequestAction.CREATE and field.exclude_from_create,
                action == RequestAction.EDIT and field.exclude_from_edit,
        )):
            continue

        # Unpack nested field containers when updating DB model
        # See admin.fields.ContainerField
        if all((
                getattr(field, "is_container", False),
                request.method.lower() != "get",
        )):
            # noinspection PyUnresolvedReferences
            arr.extend(extract_fields(request, field.fields, action))
            continue

        arr.append(field)
    return arr
