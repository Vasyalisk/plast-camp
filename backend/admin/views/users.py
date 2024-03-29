from starlette_admin import fields

import models
from admin.fields import ContainerField, DateField, DateTimeField, EnumField
from admin.views.base import TortoiseModelView
from translations import lazy_gettext as _


class UserView(TortoiseModelView):
    identity = "user"
    name = _("user")
    label = _("Users")
    model = models.User

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_list=True),
        DateTimeField("created_at", label=_("created_at"), disabled=True),
        fields.EmailField("email", label=_("email")),
        ContainerField("credentials", label=_("credentials"), fields=[
            EnumField("role", label=_("role"), choices_loader=lambda request: [
                (models.User.Role.BASE.value, str(_("BASE"))),
                (models.User.Role.ADMIN.value, str(_("ADMIN"))),
                (models.User.Role.SUPER_ADMIN.value, str(_("SUPER_ADMIN"))),
            ]),
            fields.BooleanField("is_email_verified", label=_("is_email_verified"), exclude_from_list=True),
            fields.PasswordField("password", label=_("password"), exclude_from_list=True, exclude_from_detail=True),
        ]),
        ContainerField("personal_info", label=_("personal_info"), fields=[
            fields.StringField("first_name", label=_("first_name"), exclude_from_list=True),
            fields.StringField("last_name", label=_("last_name"), exclude_from_list=True),
            fields.StringField("nickname", label=_("nickname")),
            DateField("date_of_birth", label=_("date_of_birth"), exclude_from_list=True),
        ]),
        fields.HasOne("country", label=_("country"), identity="country"),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("country")
        return queryset
