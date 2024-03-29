import typing as t
from datetime import date, datetime
from enum import Enum

import pydantic

import models
from schemas.pagination import PaginatedQuery, PaginatedResponse
from schemas.shared import CountryResponse

if t.TYPE_CHECKING:
    from schemas.camps import DetailResponse as CampResponse


class MembershipOrder(str, Enum):
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

    ROLE = "ROLE"


class MembershipQuery(PaginatedQuery):
    pass


class MembershipItemResponse(pydantic.BaseModel):
    created_at: datetime
    role: str
    camp: "CampResponse"

    class Config:
        orm_mode = True


class MembershipResponse(PaginatedResponse[MembershipItemResponse]):
    pass


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
    """
    Enum to use workaround for FastAPI issue with list in query
    https://python.plainenglish.io/how-to-use-the-new-and-cool-annotated-typing-feature-of-fastapi-4a2fdc48ef74
    """
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
