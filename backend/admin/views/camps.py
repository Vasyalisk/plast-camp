from starlette_admin import fields

import models
from admin.views.base import TortoiseModelView


class CampView(TortoiseModelView):
    model = models.Camp
    label = "Camps"
    name = "camp"
    identity = "camp"

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        fields.DateTimeField("created_at", disabled=True, exclude_from_create=True),
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
    name = "camp_member"
    identity = "camp_member"
    label = "Camp Members"

    fields = [
        fields.IntegerField("id", disabled=True, exclude_from_create=True),
        fields.DateTimeField("created_at", disabled=True, exclude_from_create=True),
        fields.EnumField("role", enum=models.CampMember.Role),
        fields.HasOne("camp", identity="camp"),
        fields.HasOne("user", identity="user"),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user", "camp")
        return queryset
