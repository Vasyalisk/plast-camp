import os.path
from typing import Dict, List, Optional, Type

from fastapi import FastAPI
from fastapi_admin import i18n
from fastapi_admin.exceptions import forbidden_error_exception, not_found_error_exception, server_error_exception
from fastapi_admin.resources import Dropdown
from fastapi_admin.resources import Model as ModelResource
from fastapi_admin.resources import Resource
from fastapi_admin.template import add_template_folder
from pydantic import HttpUrl
from redis.asyncio import Redis
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from tortoise import Model

import models
from admin import providers
from admin.routes import router
from core import redis


class FastAPIAdmin(FastAPI):
    logo_url: str
    login_logo_url: str
    admin_path: str
    resources: List[Type[Resource]] = []
    model_resources: Dict[Type[Model], Type[Resource]] = {}
    redis: Redis
    language_switch: bool = True
    favicon_url: Optional[HttpUrl] = None

    async def configure(self):
        self.redis = redis.connection
        i18n.set_locale("en_US")
        self.admin_path = "/admin"
        self.language_switch = False
        self.logo_url = "/static/admin/navbar-icon.webp"  # type: ignore
        self.logo_url ="https://preview.tabler.io/static/logo-white.svg"
        self.favicon_url = None

        ADMIN_DIR = os.path.dirname(os.path.abspath(__file__))
        add_template_folder(os.path.join(ADMIN_DIR, "templates"))

        login_provider = providers.EmailPasswordProvider(admin_model=models.User)  # type: ignore
        await login_provider.register(self)

        import admin.resources

    def register_resources(self, *resource: Type[Resource]):
        for r in resource:
            self.register(r)

    def _set_model_resource(self, resource: Type[Resource]):
        if issubclass(resource, ModelResource):
            self.model_resources[resource.model] = resource
        elif issubclass(resource, Dropdown):
            for r in resource.resources:
                self._set_model_resource(r)

    def register(self, resource: Type[Resource]):
        self._set_model_resource(resource)
        self.resources.append(resource)

    def get_model_resource(self, model: Type[Model]):
        r = self.model_resources.get(model)
        return r() if r else None

admin_app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",

)
admin_app.include_router(router)
admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)