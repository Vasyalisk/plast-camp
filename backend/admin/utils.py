import typing as t
from itertools import chain

from fastapi import Request
from starlette_admin import BaseField, RequestAction
from tortoise import Model


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


def describe_related_fields(model: t.Type[Model], related_field_names: t.List[str]) -> t.Dict[str, t.Dict[str, dict]]:
    """
    Returns described portion of specified fields as Python objects
    See https://tortoise.github.io/fields.html#tortoise.fields.base.Field.describe
    :param model:
    :param related_field_names:
    :return:
    """
    desc = model.describe(serializable=False)
    forward_it = chain(
        desc.get("fk_fields", []),
        desc.get("o2o_fields", []),
    )
    backward_it = chain(
        desc.get("backward_fk_fields", []),
        desc.get("backward_o2o_fields", []),
    )
    described = {
        "forward": {one["name"]: one for one in forward_it if one["name"] in related_field_names},
        "backward": {one["name"]: one for one in backward_it if one["name"] in related_field_names},
        "many_to_many": {one["name"]: one for one in desc.get("m2m_fields", []) if one["name"] in related_field_names},
    }
    return described


def get_related_models(
        model: t.Type[Model], related_field_names: t.List[str]
) -> t.Dict[str, t.Dict[str, Model]]:
    """
    Return related Tortoise models grouped by forward, backward and many-to-many relations.
    :param model:
    :param related_field_names:
    :return:
    """
    desc = describe_related_fields(model, related_field_names)
    return {
        "forward": {k: v["python_type"] for k, v in desc["forward"].items()},
        "backward": {k: v["python_type"] for k, v in desc["backward"].items()},
        "many_to_many": {k: v["python_type"] for k, v in desc["many_to_many"].items()},
    }
