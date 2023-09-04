from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import BaseAdmin, DropDown
from starlette_admin.i18n import I18nConfig
from starlette_admin.views import Link

import admin.views
import translations
from admin.auth import EmailAndPasswordProvider
from conf import settings
from translations import lazy_gettext as _
from translations.middleware import LocaleMiddleware


class Admin(BaseAdmin):
    def init_locale(self) -> None:
        pass

    def _setup_templates(self) -> None:
        super()._setup_templates()
        self.templates.env.globals["get_locale"] = translations.get_locale
        self.templates.env.globals["get_locale_display_name"] = translations.get_locale_display_name
        self.templates.env.globals["get_locale_display_name"] = translations.get_locale_display_name
        self.templates.env.install_gettext_callables(translations.gettext, translations.ngettext, True)


def mount_admin(app: FastAPI):
    admin_app = Admin(
        title=_("Plast Camp Admin"),
        auth_provider=EmailAndPasswordProvider(),
        middlewares=[
            Middleware(SessionMiddleware, secret_key=settings().SECRET_KEY),
            Middleware(
                LocaleMiddleware,
                default_locale=settings().TRANSLATION_DEFAULT_LOCALE,
                locales=settings().TRANSLATION_LOCALES,
            ),
        ],
        statics_dir="admin/statics",
        templates_dir="admin/templates",
        i18n_config=I18nConfig(default_locale="uk", language_switcher=settings().TRANSLATION_LOCALES),
    )
    admin_app.add_view(DropDown(
        _("Users"),
        views=[admin.views.UserView]
    ))
    admin_app.add_view(DropDown(
        _("Camps"),
        views=[
            admin.views.CampView,
            admin.views.CampMemberView,
        ]
    ))
    admin_app.add_view(DropDown(
        _("Shared"),
        views=[
            admin.views.CountryView
        ]
    ))
    admin_app.add_view(Link(_("Plast Official"), url="https://www.plast.org.ua/", target="_blank"))
    admin_app.mount_to(app)
    return admin_app
