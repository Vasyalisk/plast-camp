import typing as t

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

import models
from core import security


class EmailAndPasswordProvider(AuthProvider):
    """
    Provider to let users login to admin panel

    Only superadmins (see models.User.Role) with filled-in email are allowed
    """
    def __init__(
            self,
            login_path: str = "/login",
            logout_path: str = "/logout",
            allow_paths: t.Optional[t.Sequence[str]] = None,
    ):
        super().__init__(login_path, logout_path, allow_paths)

        if self.allow_paths is None:
            self.allow_paths = []

        # JS to support timezone
        self.allow_paths.extend([
            "/statics/js/vendor/moment.min.js",
            "/statics/js/vendor/moment-timezone-with-data-10-year-range.js",
        ])

    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        user = await models.User.get_or_none(email=username)
        if user is None:
            raise LoginFailed("Invalid username or password")

        if user.role != models.User.Role.SUPER_ADMIN:
            raise FormValidationError({"username": "User has no access to admin panel"})

        is_valid = security.verify_password(password, user.password)
        if not is_valid:
            raise LoginFailed("Invalid username or password")

        timezone: str = (await request.form()).get("timezone", "UTC")
        request.session.update({
            "token": security.Authorize().create_access_token(user.id),
            "timezone": timezone,  # store user timezone on initial login
        })
        return response

    async def is_authenticated(self, request) -> bool:
        token = request.session.get("token", None)

        if token is None:
            return False

        try:
            user = await security.Authorize(request).user_or_401(strategy=security.Authorize.Strategy.SESSION)
        except HTTPException as e:
            if e.status_code == 401:
                return False

            raise e

        if user.role != models.User.Role.SUPER_ADMIN:
            return False

        request.state.user = user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user.email)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
