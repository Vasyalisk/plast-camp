import schemas.auth
import models
from core.security import hash_password, verify_password
from fastapi import HTTPException

from fastapi_jwt_auth import AuthJWT


def raise_400(detail: str):
    raise HTTPException(status_code=400, detail={"detail": detail})


async def register(body: schemas.auth.RegisterBody) -> schemas.auth.RegisterResponse:
    body.password = hash_password(body.password)
    user = await models.User.get_or_none(email=body.email, password=None)

    if user is None:
        user = models.User(**body.dict())

    user = user.update_from_dict(body.dict())
    await user.save()

    authorize = AuthJWT()
    return schemas.auth.RegisterResponse(
        access_token=authorize.create_access_token(user.id),
        refresh_token=authorize.create_refresh_token(user.id),
    )


async def login(body: schemas.auth.LoginBody) -> schemas.auth.LoginResponse:
    user = await models.User.get_or_none(email=body.email)

    if user is None:
        raise_400("Invalid email or password")

    is_valid = verify_password(body.password, user.password)
    if not is_valid:
        raise_400("Invalid email or password")

    authorize = AuthJWT()
    return schemas.auth.LoginResponse(
        access_token=authorize.create_access_token(user.id),
        refresh_token=authorize.create_refresh_token(user.id),
    )
