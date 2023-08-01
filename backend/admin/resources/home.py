from fastapi_admin.resources import Link

from admin.app import admin_app


@admin_app.register
class HomeLink(Link):
    url = "/admin"
    label = "Home"