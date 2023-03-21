from tortoise import models, fields


class Country(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    name_ukr = fields.CharField(max_length=255)
    name_orig = fields.CharField(max_length=255)
