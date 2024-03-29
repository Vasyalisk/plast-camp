import typing as t
from datetime import date, datetime
from enum import Enum

import pydantic

from schemas.pagination import PaginatedQuery, PaginatedResponse
from schemas.shared import CountryResponse

if t.TYPE_CHECKING:
    from schemas.users import DetailResponse as UserResponse


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
    name: pydantic.constr(min_length=1)

    country_id: t.Optional[int] = None

    @pydantic.validator("date_end")
    def validate_date_end(cls, value, values):
        date_start = values.get("date_start")

        if date_start:
            assert value > date_start

        return value


class FilterQuery(PaginatedQuery):
    search: t.Optional[str] = None
    country_id: t.Optional[int] = None
    date_from: t.Optional[date] = None
    date_till: t.Optional[date] = None

    @pydantic.validator("date_till")
    def validate_date_till(cls, value, values):
        date_from = values.get("date_from")

        if value and date_from:
            assert value > date_from

        return value


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


class MembershipQuery(PaginatedQuery):
    pass


class MembershipItemResponse(pydantic.BaseModel):
    created_at: datetime
    role: str
    user: "UserResponse"

    class Config:
        orm_mode = True


class MembershipResponse(PaginatedResponse[MembershipItemResponse]):
    pass
