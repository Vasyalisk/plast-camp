from fastapi import APIRouter, Depends, Query

import schemas.users
import services.users
from core import security

router = APIRouter(tags=["users"])


@router.get("/me", response_model=schemas.users.MeResponse)
async def me(authorize: security.Authorize = Depends()):
    return await services.users.Me().get(authorize=authorize)


@router.get("/{user_id}", response_model=schemas.users.DetailResponse)
async def detail(user_id: int, authorize: security.Authorize = Depends()):
    return await services.users.Detail().get(user_id=user_id, authorize=authorize)


@router.get("", response_model=schemas.users.FilterResponse, response_model_by_alias=False)
async def filter(
        order_by: list[schemas.users.FilterOrder] = Query(default=[schemas.users.FilterOrder.CREATED_AT_DESC]),
        query: schemas.users.FilterQuery = Depends(),
        authorize: security.Authorize = Depends(),
):
    return await services.users.Filter().get(query=query, order_by=order_by, authorize=authorize)


@router.post("", response_model=schemas.users.CreateResponse, status_code=201)
async def create(body: schemas.users.CreateBody, authorize: security.Authorize = Depends()):
    return await services.users.Create().post(body=body, authorize=authorize)


@router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, authorize: security.Authorize = Depends()):
    return await services.users.Delete().delete(user_id, authorize)


@router.get("/{user_id}/membership", response_model=schemas.users.MembershipResponse)
async def membership(
        user_id: int,
        order_by: list[schemas.users.MembershipOrder] = Query(default=[schemas.users.MembershipOrder.CREATED_AT_DESC]),
        query: schemas.users.MembershipQuery = Depends(),
        authorize: security.Authorize = Depends(),
):
    return await services.users.Membership().get(user_id=user_id, order_by=order_by, query=query, authorize=authorize)
