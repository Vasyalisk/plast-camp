from starlette_admin import fields

import models
from admin.fields import ContainerField
from admin.views.base import TortoiseModelView


class UserView(TortoiseModelView):
    identity = "user"
    name = "User"
    label = "Users"
    model = models.User

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_list=True),
        fields.DateTimeField("created_at", disabled=True),
        fields.EmailField("email"),
        ContainerField("credentials", [
            fields.EnumField("role", enum=models.User.Role),
            fields.BooleanField("is_email_verified", exclude_from_list=True),
            fields.PasswordField("password", exclude_from_list=True, exclude_from_detail=True),
        ]),
        ContainerField("personal_info", [
            fields.StringField("first_name", exclude_from_list=True),
            fields.StringField("last_name", exclude_from_list=True),
            fields.StringField("nickname"),
            fields.DateField("date_of_birth", exclude_from_list=True),
            fields.IntegerField("country_id", disabled=True, exclude_from_list=True),
        ]),
    ]
