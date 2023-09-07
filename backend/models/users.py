from enum import Enum

from fastapi import Request
from tortoise import fields, models

from translations import lazy_gettext as _


class User(models.Model):
    """
    Application user
    """

    class Role(str, Enum):
        """
        User role

        SUPER_ADMIN - can add, edit and create users without restrictions
        ADMIN - can create, edit and delete camps and partially edit own user
        BASE - can add or remove itself to/from existing camps
        """
        SUPER_ADMIN = "SUPER_ADMIN"
        ADMIN = "ADMIN"
        BASE = "BASE"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    email = fields.CharField(
        max_length=320,
        null=True,
        default=None,
        unique=True,
        description="Required for users to login and optional otherwise",
    )
    is_email_verified = fields.BooleanField(default=False)
    password = fields.CharField(max_length=255, null=True, default=None, description="Hashed password")

    first_name = fields.CharField(max_length=127, default="")
    last_name = fields.CharField(max_length=127, default="")
    nickname = fields.CharField(max_length=127, default="")
    date_of_birth = fields.DateField(null=True)

    role = fields.CharEnumField(Role, max_length=64, default=Role.BASE)

    country = fields.ForeignKeyField(
        "models.Country", null=True, default=None, on_delete=fields.SET_NULL, related_name="users"
    )

    def full_name(self) -> str:
        return " ".join(one for one in (self.first_name, self.last_name) if one)

    async def __admin_repr__(self, request: Request) -> str:
        return self.nickname or self.full_name() or str(self.id)

    async def __admin_select2_repr__(self, request: Request) -> str:
        return (
            "<span>"
            f"{_('nickname').capitalize()}: {self.nickname or '...'}, "
            f"{_('name')}: {self.full_name() or '...'}, "
            f"id: {self.id}</span>"
        )
