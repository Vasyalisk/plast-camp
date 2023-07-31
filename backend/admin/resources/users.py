from fastapi_admin import resources
from fastapi_admin.widgets import displays, filters, inputs

import models
from admin.app import admin_app


@admin_app.register
class UserAdmin(resources.Model):
    label = "Users"
    model = models.User
    fields = (
        "id",
        resources.Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        resources.Field(
            name="email",
            label="Email",
            input_=inputs.Email(),
        ),
        "is_email_verified",
        "first_name",
        "last_name",
    )
