from tortoise import Model, fields


class AbstractEmailAdmin(Model):
    email = fields.CharField(max_length=320, unique=True, null=True, default=None)
    password = fields.CharField(max_length=255, null=True, default=None)

    class Meta:
        abstract = True
