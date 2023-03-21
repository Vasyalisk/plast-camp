from tortoise import models, fields
from enum import Enum


class Camp(models.Model):
    """
    Табір або інша пластова акція
    """
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Додано")

    date_start = fields.DateField(null=True, description="Дата початку")
    date_end = fields.DateField(null=True, description="Дата закінчення")

    description = fields.CharField(max_length=1024, description="Короткий опис")
    location = fields.CharField(max_length=255, description="Місце проведення")
    name = fields.CharField(max_length=255, description="Назва")

    country = fields.ForeignKeyField(
        "models.Country", on_delete=fields.SET_NULL, null=True, default=None, description="Край"
    )

    # TODO: add url to badge image if any


class CampMember(models.Model):
    """
    Член табору, може бути як член проводу, так і учасник / гість
    """

    class Role(str, Enum):
        """
        Роль члена табору

        STAFF - провід
        PARTICIPANT - учасник
        GUEST - гість
        """
        STAFF = "STAFF"
        PARTICIPANT = "PARTICIPANT"
        GUEST = "GUEST"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Додано")

    role = fields.CharEnumField(Role, max_length=64, description="Роль (провід, учасник, гість)")

    camp = fields.ForeignKeyField(
        "models.Camp", on_delete=fields.CASCADE, related_name="members", description="Табір / акція"
    )
    user = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="members", description="Користувач"
    )
