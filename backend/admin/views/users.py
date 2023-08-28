from starlette_admin import fields

import models
from admin.views.base import TortoiseModelView


class UserView(TortoiseModelView):
    identity = "user"
    name = "User"
    label = "Користувачі"
    model = models.User

    fields = [
        fields.IntegerField("id", read_only=True),
        fields.DateTimeField("created_at", read_only=True),
        fields.EmailField("email"),
        fields.BooleanField("is_email_verified"),
        fields.PasswordField("password"),
        fields.StringField("first_name"),
        fields.StringField("last_name"),
        fields.StringField("nickname"),
        fields.DateField("date_of_birth"),
        fields.EnumField("role", enum=models.User.Role),
        fields.IntegerField("country_id", read_only=True),
    ]
