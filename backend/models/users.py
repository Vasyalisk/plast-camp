from enum import Enum

from tortoise import fields, models


class User(models.Model):
    """
    Користувач
    """

    # TODO: add fine-grained permissions if needed
    class Role(str, Enum):
        """
        Роль користувача

        SUPER_ADMIN - може додавати, редагувати і створювати користувачів без обмежень
        ADMIN - може створювати, редагувати і видаляти табори / акції і обмежено редагувати власного користувача
        BASE - може додаватися / видялятися з існуючих таборів
        """
        SUPER_ADMIN = "SUPER_ADMIN"
        ADMIN = "ADMIN"
        BASE = "BASE"

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Додано")

    email = fields.CharField(
        max_length=320,
        null=True,
        default=None,
        unique=True,
        description="Обов'язкове поле для користувачів, що хочуть мати змогу залогінитись",
    )
    is_email_verified = fields.BooleanField(default=False, description="Чи дійсний емейл?")
    password = fields.CharField(max_length=255, null=True, default=None, description="Хешований пароль")

    first_name = fields.CharField(max_length=127, description="Ім'я", default="")
    last_name = fields.CharField(max_length=127, description="Прізвище", default="")
    nickname = fields.CharField(max_length=127, description="Псевдо", default="")
    date_of_birth = fields.DateField(null=True, description="Дата народження")

    role = fields.CharEnumField(Role, max_length=64, default=Role.BASE, description="Роль користувача")

    country = fields.ForeignKeyField(
        "models.Country", null=True, default=None, on_delete=fields.SET_NULL, related_name="users", description="Край"
    )

    @property
    def username(self) -> str:
        return self.email