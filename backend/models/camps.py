from enum import Enum

from fastapi import Request
from tortoise import fields, models


class Camp(models.Model):
    """
    Camp or other scout meeting
    """
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    date_start = fields.DateField(null=True)
    date_end = fields.DateField(null=True)

    description = fields.CharField(max_length=1024)
    location = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)

    country = fields.ForeignKeyField("models.Country", on_delete=fields.SET_NULL, null=True, default=None)

    # TODO: add url to badge image if any

    async def __admin_repr__(self, request: Request) -> str:
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        text = self.name

        if self.date_start is None and self.date_end is None:
            return f"<span>{text}</span>"

        date_start = "..."
        date_end = "..."

        if self.date_start:
            date_start = self.date_start.isoformat()

        if self.date_end:
            date_end = self.date_end.isoformat()

        return f"<span>{text}: {date_start} - {date_end}</span>"


class CampMember(models.Model):
    """
    Camp participant: can be staff as well as guest / plain participant
    """

    class Role(str, Enum):
        STAFF = "STAFF"
        PARTICIPANT = "PARTICIPANT"
        GUEST = "GUEST"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    role = fields.CharEnumField(Role, max_length=64)

    camp = fields.ForeignKeyField("models.Camp", on_delete=fields.CASCADE, related_name="members")
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="membership")

    class Meta:
        unique_together = ("camp_id", "user_id")

    async def __admin_repr__(self, request: Request) -> str:
        user = self.user

        if isinstance(user, models.QuerySet):
            user = await self.user

        return await user.__admin_repr__(request)

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<span>{await self.camp.__admin_repr__(request)} - {await self.user.__admin_repr__(request)}</span>"
