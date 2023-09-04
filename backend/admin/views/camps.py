from starlette_admin import fields

import models
from admin.fields import AwareDateTimeField
from admin.views.base import TortoiseModelView
from translations import lazy_gettext as _


class CampView(TortoiseModelView):
    model = models.Camp
    label = _("Camps")
    name = _("camp")
    identity = "camp"

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        AwareDateTimeField("created_at", disabled=True, exclude_from_create=True),
        fields.DateField("date_start"),
        fields.DateField("date_end"),
        fields.TextAreaField("description", maxlength=1024),
        fields.StringField("location", maxlength=255),
        fields.StringField("name", maxlength=255),
        fields.HasOne("country", identity="country"),
        fields.HasMany("members", identity="camp_member")
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
        AwareDateTimeField("created_at", disabled=True, exclude_from_create=True),
        fields.EnumField("role", enum=models.CampMember.Role),
        fields.HasOne("camp", identity="camp"),
        fields.HasOne("user", identity="user"),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user", "camp")
        return queryset
