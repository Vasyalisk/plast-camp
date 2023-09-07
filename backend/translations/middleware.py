import typing as t

from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Receive, Scope, Send

from translations.utils import set_locale


class LocaleMiddleware:
    """
    Middleware to set request locale

    Default one is used if locale is not in the allowed list
    """
    def __init__(
            self,
            app: ASGIApp,
            language_header: t.Optional[str] = "Accept-Language",
            language_cookie: t.Optional[str] = "language",
            locales: t.Optional[t.List[str]] = None,
            default_locale: t.Optional[str] = "en",
    ) -> None:
        if locales is None:
            locales = ["en"]

        self.app = app
        self.language_header = language_header
        self.language_cookie = language_cookie
        self.default_locale = default_locale
        self.locales = locales

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        conn = HTTPConnection(scope)
        locale: t.Optional[str] = self.default_locale
        if (
                self.language_cookie
                and conn.cookies.get(self.language_cookie, None)
                in self.locales
        ):
            # detect locale in cookies
            locale = conn.cookies.get(self.language_cookie)
        elif (
                self.language_header
                and conn.headers.get(self.language_header, None)
                in self.locales
        ):
            # detect locale in headers
            locale = conn.headers.get(self.language_header)
        set_locale(locale or self.default_locale)
        await self.app(scope, receive, send)
