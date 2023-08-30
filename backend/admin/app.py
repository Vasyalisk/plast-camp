from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import BaseAdmin as Admin

import admin.views
from admin.auth import EmailAndPasswordProvider
from conf import settings


def mount_admin(app: FastAPI):
    admin_app = Admin(
        auth_provider=EmailAndPasswordProvider(),
        middlewares=[Middleware(SessionMiddleware, secret_key=settings().SECRET_KEY)]
    )
    admin_app.add_view(admin.views.UserView)
    admin_app.add_view(admin.views.CountryView)
    admin_app.add_view(admin.views.CampView)
    admin_app.add_view(admin.views.CampMemberView)
    admin_app.mount_to(app)
    return admin_app
