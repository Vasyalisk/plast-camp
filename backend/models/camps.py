from tortoise import models, fields
from enum import Enum


class Camp(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    date_start = fields.DateField(null=True)
    date_end = fields.DateField(null=True)

    description = fields.CharField(max_length=1024)
    location = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)

    # TODO: add url to badge image if any


class CampMember(models.Model):
    class Role(str, Enum):
        STAFF = "STAFF"
        PARTICIPANT = "PARTICIPANT"
        GUEST = "GUEST"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    role = fields.CharEnumField(Role, max_length=64)

    camp = fields.ForeignKeyField("models.Camp", on_delete=fields.CASCADE, related_name="members")
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="members")
