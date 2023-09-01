from starlette_admin import fields

import models
from admin.fields import AwareDateTimeField
from admin.views.base import TortoiseModelView


class CountryView(TortoiseModelView):
    model = models.Country
    identity = "country"
    name = "country"
    label = "Countries"

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        AwareDateTimeField("created_at", disabled=True, exclude_from_create=True),
        fields.StringField("name_ukr", maxlength=255),
        fields.StringField("name_orig", maxlength=255),
    ]