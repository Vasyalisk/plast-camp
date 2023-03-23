import schemas.auth
import models
import redis
from core import redis, security, mail, errors

from services.base import BaseService


class Register(BaseService):
    async def post(self, body: schemas.auth.RegisterBody) -> schemas.auth.RegisterResponse:
        body.password = security.hash_password(body.password)
        user = await self.get_or_create_user(body)

        code = await redis.generate_code(user.id, redis.CodeType.REGISTER)
        await mail.send(mail.EmailType.REGISTRATION, code=code)

        authorize = security.Authorize()
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


class ConfirmRegistration(BaseService):
    async def patch(self, body: schemas.auth.ConfirmRegistrationBody) -> None:
        user_id = await self.user_id_or_400(body.code)
        user = await self.user_or_400(user_id)
        user.is_email_verified = True
        await user.save()

    async def user_id_or_400(self, code) -> int:
        user_id = await redis.check_code(code, redis.CodeType.REGISTER)

        if user_id is None:
            self.raise_400(errors.INVALID_CODE)

        await redis.delete_code(code, redis.CodeType.REGISTER)

        try:
            user_id = int(user_id)
        except ValueError:
            self.raise_400(errors.INVALID_CODE)

        return user_id

    async def user_or_400(self, user_id) -> models.User:
        user = await models.User.get_or_none(id=user_id)

        if user is None:
            self.raise_400(errors.INVALID_CODE)

        return user


class Login(BaseService):
    async def post(self, body: schemas.auth.LoginBody) -> schemas.auth.LoginResponse:
        user = await self.user_or_401(body.email)
        self.validate_password(body.password, user.password)

        authorize = security.Authorize()
        return schemas.auth.LoginResponse(
            access_token=authorize.create_access_token(user.id),
            refresh_token=authorize.create_refresh_token(user.id),
        )

    async def user_or_401(self, email: str) -> models.User:
        user = await models.User.get_or_none(email=email)

        if user is None:
            self.raise_401(errors.INVALID_LOGIN)

        return user

    def validate_password(self, plain_password: str, hashed_password: str):
        is_valid = security.verify_password(plain_password, hashed_password)

        if not is_valid:
            self.raise_401(errors.INVALID_LOGIN)


class ChangePassword(BaseService):
    async def patch(self, body: schemas.auth.ChangePasswordBody, authorize: security.Authorize) -> None:
        user = await authorize.user_or_401()
        self.validate_password(body.old_password, user.password)
        user.password = security.hash_password(body.new_password)
        await user.save()

    def validate_password(self, plain_password: str, hashed_password: str):
        is_valid = security.verify_password(plain_password, hashed_password)

        if not is_valid:
            self.raise_401(errors.INVALID_PASSWORD)


class ForgotPassword(BaseService):
    async def post(self, body: schemas.auth.ForgotPasswordBody) -> None:
        user = await models.User.get_or_none(email=body.email)

        if user is None:
            return

        code = await redis.generate_code(user.id, redis.CodeType.FORGOT_PASSWORD)
        await mail.send(mail.EmailType.FORGOT_PASSWORD, code=code)


class ResetPassword(BaseService):
    async def post(self, body: schemas.auth.ResetPasswordBody) -> None:
        user_id = await self.user_id_or_400(body.code)
        user = await self.user_or_400(user_id)
        user.password = security.hash_password(body.password)
        await user.save()

    # noinspection DuplicatedCode
    async def user_id_or_400(self, code):
        user_id = await redis.check_code(code, redis.CodeType.FORGOT_PASSWORD)

        if user_id is None:
            self.raise_400(errors.INVALID_CODE)

        await redis.delete_code(code, redis.CodeType.FORGOT_PASSWORD)

        try:
            user_id = int(user_id)
        except ValueError:
            self.raise_400(errors.INVALID_CODE)

        return user_id

    async def user_or_400(self, user_id) -> models.User:
        user = await models.User.get_or_none(id=user_id)

        if user is None:
            self.raise_400(errors.INVALID_CODE)

        return user
