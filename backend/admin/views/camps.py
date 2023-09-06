from starlette_admin import fields

import models
from admin.fields import DateField, DateTimeField, EnumField
from admin.views.base import TortoiseModelView
from translations import lazy_gettext as _


class CampView(TortoiseModelView):
    model = models.Camp
    label = _("Camps")
    name = _("camp")
    identity = "camp"

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        DateTimeField("created_at", label=_("created_at"), disabled=True, exclude_from_create=True),
        DateField("date_start", label=_("date_start")),
        DateField("date_end", label=_("date_end")),
        fields.TextAreaField("description", label=_("description"), maxlength=1024),
        fields.StringField("location", label=_("location"), maxlength=255),
        fields.StringField("name", label=_("name"), maxlength=255),
        fields.HasOne("country", label=_("country"), identity="country"),
        fields.HasMany("members", label=_("members"), identity="camp_member")
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("country").prefetch_related("members")
        return queryset


class CampMemberView(TortoiseModelView):
    model = models.CampMember
    name = _("participant")
    identity = "camp_member"
    label = _("Participants")

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        DateTimeField("created_at", label=_("created_at"), disabled=True, exclude_from_create=True),
        EnumField("role", label=_("role"), choices_loader=lambda request: [
            (models.CampMember.Role.GUEST.value, str(_("GUEST"))),
            (models.CampMember.Role.PARTICIPANT.value, str(_("PARTICIPANT"))),
            (models.CampMember.Role.STAFF.value, str(_("STAFF"))),
        ]),
        fields.HasOne("camp", label=_("camp"), identity="camp"),
        fields.HasOne("user", label=_("user"), identity="user"),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user", "camp")
        return queryset
