from starlette_admin import BaseAdmin as Admin
from fastapi import FastAPI
import admin.views


def mount_admin(app: FastAPI):
    admin_app = Admin()
    admin_app.add_view(admin.views.UserView)
    admin_app.mount_to(app)
    return admin_app
