import typing as t
from datetime import date, datetime
from enum import Enum

import pydantic

import models
from schemas.pagination import PaginatedQuery, PaginatedResponse


class CountryResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    name_ukr: str
    name_orig: str

    class Config:
        orm_mode = True


class CampResponse(pydantic.BaseModel):
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


class MembershipResponse(pydantic.BaseModel):
    created_at: datetime
    role: str
    camp: CampResponse

    class Config:
        orm_mode = True


class MeResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    email: str
    is_email_verified: bool

    first_name: str
    last_name: str
    nickname: str
    date_of_birth: t.Optional[date]
    role: str

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class DetailResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    first_name: str
    last_name: str
    nickname: str
    date_of_birth: t.Optional[date]
    role: str

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class FilterItemResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    first_name: str
    last_name: str
    nickname: str

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class FilterOrder(str, Enum):
    CREATED_AT_ASC = "CREATED_AT_ASC"
    CREATED_AT_DESC = "CREATED_AT_DESC"

    AGE_ASC = "AGE_ASC"
    AGE_DESC = "AGE_DESC"

    COUNTRY_ASC = "COUNTRY_ASC"
    COUNTRY_DESC = "COUNTRY_DESC"

    ROLE = "ROLE"


class FilterQuery(PaginatedQuery):
    search: t.Optional[str] = None
    role: t.Optional[models.User.Role] = None
    membership__role: t.Optional[models.CampMember.Role] = pydantic.Field(default=None, alias="camp_role")
    country_id: t.Optional[int] = None

    age: t.Optional[int] = None
    age__gte: t.Optional[int] = None
    age__lte: t.Optional[int] = None

    @pydantic.root_validator(pre=True)
    def validate_model(cls, values):
        age_comparison = values.get("age__gte", values.get("age__lte"))
        age = values.get("age")

        assert not (age_comparison and age)
        return values


class FilterResponse(PaginatedResponse[FilterItemResponse]):
    pass


class CreateBody(pydantic.BaseModel):
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    nickname: str = ""
    date_of_birth: t.Optional[date] = None
    role: models.User.Role = models.User.Role.BASE
    country_id: t.Optional[int] = None


class CreateResponse(DetailResponse):
    pass
