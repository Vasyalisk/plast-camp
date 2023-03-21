from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    email = fields.CharField(max_length=320, null=True, default=None, unique=True)
    first_name = fields.CharField(max_length=127)
    last_name = fields.CharField(max_length=127)
    nickname = fields.CharField(max_length=127)
    date_of_birth = fields.DateField(null=True)

    country = fields.ForeignKeyField(
        "models.Country", null=True, default=None, on_delete=fields.SET_NULL, related_name="users"
    )
