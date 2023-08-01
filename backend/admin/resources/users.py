from fastapi_admin import resources
from fastapi_admin.widgets import displays, inputs

import models
from admin.app import admin_app
from admin.resources.utils import setup_read_only_fields


@admin_app.register
@setup_read_only_fields(
    "id",
    "created_at",
)
class UserAdmin(resources.Model):
    label = "Users"
    model = models.User
    fields = (
        "id",
        "created_at",
        resources.Field(
            name="email",
            input_=inputs.Email(),
        ),
        "is_email_verified",
        resources.Field(
            name="password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),

        "first_name",
        "last_name",
        "nickname",
        "date_of_birth",
        "role",
        "country",
    )
