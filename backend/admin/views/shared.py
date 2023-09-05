from starlette_admin import fields

import models
from admin.fields import AwareDateTimeField
from admin.views.base import TortoiseModelView
from translations import lazy_gettext as _


class CountryView(TortoiseModelView):
    model = models.Country
    identity = "country"
    name = _("country")
    label = _("Countries")

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        AwareDateTimeField("created_at", label=_("created_at"), disabled=True, exclude_from_create=True),
        fields.StringField("name_ukr", label=_("name_ukr"), maxlength=255),
        fields.StringField("name_orig", label=_("name_orig"), maxlength=255),
    ]