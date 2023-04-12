import typing as t
from datetime import datetime

import pydantic

from schemas.pagination import PaginatedQuery, PaginatedResponse


class CountryResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    name_ukr: str
    name_orig: str

    class Config:
        orm_mode = True


class CountryFilterQuery(PaginatedQuery):
    search: t.Optional[str] = None


class CountryFilterItemResponse(pydantic.BaseModel):
    id: int

    name_ukr: str
    name_orig: str

    class Config:
        orm_mode = True


class CountryFilterResponse(PaginatedResponse[CountryFilterItemResponse]):
    pass
