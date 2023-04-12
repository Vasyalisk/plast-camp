import typing as t
from datetime import date, datetime
from enum import Enum

import pydantic

from schemas.pagination import PaginatedQuery, PaginatedResponse
from schemas.shared import CountryResponse


class DetailResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    date_start: t.Optional[date]
    date_end: t.Optional[date]

    description: str
    location: str
    name: str

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class CreateBody(pydantic.BaseModel):
    date_start: t.Optional[date] = None
    date_end: t.Optional[date] = None

    description: str
    location: str
    name: str

    country_id: t.Optional[int] = None


class FilterQuery(PaginatedQuery):
    search: t.Optional[str] = None
    country_id: t.Optional[int] = None
    date_from: t.Optional[date] = None
    date_till: t.Optional[date] = None


class FilterItemResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    date_start: t.Optional[date]
    date_end: t.Optional[date]

    name: str

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class FilterOrder(str, Enum):
    """
    Enum to use workaround for FastAPI issue with list in query
    https://python.plainenglish.io/how-to-use-the-new-and-cool-annotated-typing-feature-of-fastapi-4a2fdc48ef74
    """

    CREATED_AT_ASC = "CREATED_AT_ASC"
    CREATED_AT_DESC = "CREATED_AT_DESC"

    DATE_START_ASC = "DATE_START_ASC"
    DATE_START_DESC = "DATE_START_DESC"

    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"

    COUNTRY_ASC = "COUNTRY_ASC"
    COUNTRY_DESC = "COUNTRY_DESC"


class FilterResponse(PaginatedResponse[FilterItemResponse]):
    pass
