from fastapi import APIRouter, Depends

import schemas.shared
from core import security

router = APIRouter(tags=["shared"])


@router.get("/countries", response_model=schemas.shared.CountryFilterResponse)
async def country_filter(
        query: schemas.shared.CountryFilterQuery = Depends(),
        authorize: security.Authorize = Depends()
):
    pass
