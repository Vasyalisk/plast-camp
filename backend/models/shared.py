from fastapi import Request
from tortoise import fields, models


class Country(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    name_ukr = fields.CharField(max_length=255)
    name_orig = fields.CharField(max_length=255)

    def __str__(self):
        return self.name_ukr

    async def __admin_repr__(self, request: Request) -> str:
        return self.name_ukr

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<span>{self.name_ukr} - {self.name_orig}</span>"
