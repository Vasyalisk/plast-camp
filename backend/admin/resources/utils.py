import typing as t

from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, inputs


def setup_read_only_fields(*field_names: str):
    """
    Search for all field names which are marked as read-only and replace found strings with display-only widgets
    :return:
    """

    def wrapper(cls: t.Type[Model]):
        if not field_names:
            return

        pk_column = cls.model._meta.db_pk_column
        cls.fields = list(cls.fields)

        for name in field_names:
            try:
                i = cls.fields.index(name)
            except ValueError:
                continue

            if name == pk_column:
                continue

            cls.fields[i] = Field(name=name, input_=inputs.DisplayOnly())

        return cls

    return wrapper


def setup_write_only_fields(*field_names):
    """
    Search for all field names which are marked as write-only and replace found strings with input-only widgets
    :return:
    """
    def wrapper(cls: t.Type[Model]):
        if not field_names:
            return

        pk_column = cls.model._meta.db_pk_column
        cls.fields = list(cls.fields)

        for name in field_names:
            try:
                i = cls.fields.index(name)
            except ValueError:
                continue

            assert name != pk_column, f"Primary key can not be writeable: {name}"
            cls.fields[i] = Field(name=name, display=displays.InputOnly())

        return cls

    return wrapper
