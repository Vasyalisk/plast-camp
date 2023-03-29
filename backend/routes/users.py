from fastapi import APIRouter, Depends
import schemas.users
from core import security
import services.users

router = APIRouter(tags=["users"])


@router.get("/me", response_model=schemas.users.MeResponse)
async def me(authorize: security.Authorize = Depends()):
    return await services.users.Me().get(authorize=authorize)


@router.get("/{user_id}", response_model=schemas.users.DetailResponse)
async def detail(user_id: int, authorize: security.Authorize = Depends()):
    return await services.users.Detail().get(user_id=user_id, authorize=authorize)


@router.get("", response_model=schemas.users.FilterResponse, response_model_by_alias=False)
async def filter(query: schemas.users.FilterQuery = Depends(), authorize: security.Authorize = Depends()):
    return await services.users.Filter().get(query=query, authorize=authorize)
