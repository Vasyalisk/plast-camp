from tortoise import fields, models


class Country(models.Model):
    """
    Пластовий край
    """
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Додано")

    name_ukr = fields.CharField(max_length=255, description="Назва українською")
    name_orig = fields.CharField(max_length=255, description="Самоназва країни")
