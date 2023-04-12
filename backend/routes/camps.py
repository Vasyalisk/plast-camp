from fastapi import APIRouter, Depends, Query

import schemas.camps
from core import security

router = APIRouter(tags=["camps"])


@router.get("/{camp_id}", response_model=schemas.camps.DetailResponse)
async def detail(camp_id: int, authorize: security.Authorize = Depends()):
    pass


@router.post("", response_model=schemas.camps.DetailResponse)
async def create(body: schemas.camps.CreateBody, authorize: security.Authorize = Depends()):
    pass


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
        authorize: security.Authorize = Depends(),
):
    pass
