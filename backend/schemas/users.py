from pydantic import BaseModel
from datetime import datetime, date

import typing as t


class UserCountry(BaseModel):
    id: int
    created_at: datetime

    name_ukr: str
    name_orig: str


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

    country: t.Optional[UserCountry]
