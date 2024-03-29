import typing as t
from enum import Enum

import bcrypt
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

import models
from conf import settings


class JwtConfig(BaseModel):
    authjwt_secret_key: str = settings().SECRET_KEY
    authjwt_access_token_expires: int = settings().ACCESS_TOKEN_EXPIRES
    authjwt_refresh_token_expires: int = settings().REFRESH_TOKEN_EXPIRES

# Dependency to parse Authorization header
AuthorizationHeader = APIKeyHeader(name="Authorization", auto_error=False)


# Dependency to authenticate and authorize user based on Authorization header or cookies
class Authorize(AuthJWT):
    class Strategy(str, Enum):
        ACCESS_TOKEN = "ACCESS_TOKEN"
        REFRESH_TOKEN = "REFRESH_TOKEN"
        SESSION = "SESSION"

    def __init__(self, req: Request = None, res: Response = None):
        super().__init__(req=req, res=res)
        self._request = req

    def raise_401(self, detail: t.Optional[str] = None):
        raise HTTPException(status_code=401, detail=detail)

    async def user_or_401(self, strategy: t.Optional[Strategy] = Strategy.ACCESS_TOKEN) -> models.User:
        self._authorize(strategy)
        user_id = self.get_jwt_subject()
        user = await models.User.get_or_none(id=user_id)

        if user is None:
            self.raise_401()

        return user

    def _authorize(self, strategy: Strategy):
        method_map = {
            Authorize.Strategy.ACCESS_TOKEN: self.jwt_required,
            Authorize.Strategy.REFRESH_TOKEN: self.jwt_refresh_token_required,
            Authorize.Strategy.SESSION: self.jwt_session_required,
        }
        try:
            method_map[strategy]()
        except AuthJWTException as e:
            self.raise_401()

    def jwt_session_required(self):
        self._token = self._request.session.get("token", None)
        if self._token is None:
            self.raise_401()

        self._verify_jwt_in_request(self._token, "access", 'cookies')


def configure_jwt(app: FastAPI):
    AuthJWT.load_config(JwtConfig)  # type: ignore


def hash_password(password: str) -> str:
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")

    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except ValueError:
        return False
