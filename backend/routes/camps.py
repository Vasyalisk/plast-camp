from fastapi import APIRouter, Depends, Query

import schemas.camps
import services.camps
from core import security

router = APIRouter(tags=["camps"])


@router.get("/{camp_id}", response_model=schemas.camps.DetailResponse)
async def detail(camp_id: int, authorize: security.Authorize = Depends()):
    return await services.camps.Detail().get(camp_id=camp_id, authorize=authorize)


@router.post("", response_model=schemas.camps.DetailResponse, status_code=201)
async def create(body: schemas.camps.CreateBody, authorize: security.Authorize = Depends()):
    return await services.camps.Create().post(body=body, authorize=authorize)


@router.delete("/{camp_id}", status_code=204)
async def delete(camp_id: int, authorize: security.Authorize = Depends()):
    pass


@router.get("", response_model=schemas.camps.FilterResponse)
async def filter(
        order_by: list[schemas.camps.FilterOrder] = Query(default=[schemas.camps.FilterOrder.NAME_ASC]),
        query: schemas.camps.FilterQuery = Depends(),
        authorize: security.Authorize = Depends(),
):
    pass


@router.get("/my", response_model=schemas.camps.FilterResponse)
async def my(
        order_by: list[schemas.camps.FilterOrder] = Query(default=[schemas.camps.FilterOrder.NAME_ASC]),
        query: schemas.camps.MembershipQuery = Depends(),
        authorize: security.Authorize = Depends(),
):
    pass


@router.get("/{camp_id}/membership", response_model=schemas.camps.MembershipResponse)
async def membership(query: schemas.camps.MembershipQuery = Depends(), authorize: security.Authorize = Depends()):
    pass
