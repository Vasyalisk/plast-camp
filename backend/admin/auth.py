from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

import models
from core import security


class EmailAndPasswordProvider(AuthProvider):
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

        if user.role != models.User.Role.ADMIN:
            raise FormValidationError({"username": "User has no access to admin panel"})

        is_valid = security.verify_password(password, user.password)
        if not is_valid:
            raise LoginFailed("Invalid username or password")

        request.session.update({"token": security.Authorize().create_access_token(user.id)})
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

        if user.role != models.User.Role.ADMIN:
            return False

        request.state.user = user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user.email)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
