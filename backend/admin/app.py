from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import BaseAdmin as Admin
from starlette_admin import DropDown
from starlette_admin.views import Link

import admin.views
from admin.auth import EmailAndPasswordProvider
from conf import settings


def mount_admin(app: FastAPI):
    admin_app = Admin(
        title="Plast Camp Admin",
        auth_provider=EmailAndPasswordProvider(),
        middlewares=[Middleware(SessionMiddleware, secret_key=settings().SECRET_KEY)]
    )
    admin_app.add_view(DropDown(
        "Users",
        views=[admin.views.UserView]
    ))
    admin_app.add_view(DropDown(
        "Camps",
        views=[
            admin.views.CampView,
            admin.views.CampMemberView,
        ]
    ))
    admin_app.add_view(DropDown(
        "Shared",
        views=[
            admin.views.CountryView
        ]
    ))
    admin_app.add_view(Link("Plast Official", url="https://www.plast.org.ua/", target="_blank"))
    admin_app.mount_to(app)
    return admin_app
