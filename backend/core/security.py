from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from conf import settings
import bcrypt


class JwtConfig(BaseModel):
    authjwt_secret_key: str = settings().SECRET_KEY
    authjwt_access_token_expires: int = settings().ACCESS_TOKEN_EXPIRES
    authjwt_refresh_token_expires: int = settings().REFRESH_TOKEN_EXPIRES


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
    return bcrypt.checkpw(plain_password, hashed_password)
