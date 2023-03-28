from pydantic import BaseModel, validator, root_validator
from datetime import datetime, date

import typing as t
import models
from schemas.pagination import PaginatedResponse, PaginatedQuery


class CountryResponse(BaseModel):
    id: int
    created_at: datetime

    name_ukr: str
    name_orig: str

    class Config:
        orm_mode = True


class CampResponse(BaseModel):
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


class MembershipResponse(BaseModel):
    created_at: datetime
    role: str
    camp: CampResponse

    class Config:
        orm_mode = True


class MeResponse(BaseModel):
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


class DetailResponse(BaseModel):
    id: int
    created_at: datetime

    first_name: str
    last_name: str
    nickname: str
    date_of_birth: t.Optional[date]
    role: str

    country: t.Optional[CountryResponse]
    membership: t.List[MembershipResponse]

    class Config:
        orm_mode = True

    @validator("membership", pre=True)
    def validate_related_field(cls, value):
        if isinstance(value, list):
            return value

        return list(value)


class FilterItemResponse(BaseModel):
    id: int
    created_at: datetime

    first_name: str
    last_name: str
    nickname: str
    date_of_birth: t.Optional[date]

    country: t.Optional[CountryResponse]

    class Config:
        orm_mode = True


class FilterQuery(PaginatedQuery):
    search: t.Optional[str] = None
    role: t.Optional[models.User.Role] = None
    camp_role: t.Optional[models.CampMember.Role] = None
    country_id: t.Optional[int] = None

    age: t.Optional[int] = None
    age__gte: t.Optional[int] = None
    age__lte: t.Optional[int] = None

    @root_validator(pre=True)
    def validate_model(cls, values):
        age_comparison = values.get("age__gte", values.get("age__lte"))
        age = values.get("age")

        assert not (age_comparison and age)
        return values


class FilterResponse(PaginatedResponse[FilterItemResponse]):
    pass
