from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from conf import settings


class JwtConfig(BaseModel):
    authjwt_secret_key: str = settings().SECRET_KEY
    authjwt_access_token_expires: int = settings().ACCESS_TOKEN_EXPIRES
    authjwt_refresh_token_expires: int = settings().REFRESH_TOKEN_EXPIRES


def configure_jwt(app: FastAPI):
    AuthJWT.load_config(JwtConfig)  # type: ignore
