import schemas.auth
import models

from fastapi_jwt_auth import AuthJWT


async def register(body: schemas.auth.RegisterBody) -> schemas.auth.RegisterResponse:
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
