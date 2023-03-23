import schemas.auth
import models
from core import redis, security

from services.base import BaseService
from fastapi_jwt_auth import AuthJWT


class Register(BaseService):
    async def post(self, body: schemas.auth.RegisterBody) -> schemas.auth.RegisterResponse:
        body.password = security.hash_password(body.password)
        user = await self.get_or_create_user(body)

        await redis.generate_code(user.id, redis.CodeType.REGISTER)

        authorize = AuthJWT()
        return schemas.auth.RegisterResponse(
            access_token=authorize.create_access_token(user.id),
            refresh_token=authorize.create_refresh_token(user.id),
        )

    async def get_or_create_user(self, body: schemas.auth.RegisterBody) -> models.User:
        user = await models.User.get_or_none(email=body.email, password=None)

        if user is None:
            user = models.User(**body.dict())

        user = user.update_from_dict(body.dict())
        await user.save()
        return user


class Login(BaseService):
    async def post(self, body: schemas.auth.LoginBody) -> schemas.auth.LoginResponse:
        user = await models.User.get_or_none(email=body.email)

        if user is None:
            self.raise_401("Invalid email or password")

        is_valid = security.verify_password(body.password, user.password)
        if not is_valid:
            self.raise_401("Invalid email or password")

        authorize = AuthJWT()
        return schemas.auth.LoginResponse(
            access_token=authorize.create_access_token(user.id),
            refresh_token=authorize.create_refresh_token(user.id),
        )
