from pydantic import BaseModel, EmailStr, validator
import typing as t
from schemas.validators import validate_password

from datetime import date


class RegisterBody(BaseModel):
    email: EmailStr
    password: str

    first_name: t.Optional[str] = ""
    last_name: t.Optional[str] = ""
    nickname: t.Optional[str] = ""
    date_of_birth: t.Optional[date]
    country_id: t.Optional[int]

    @validator("email")
    def validate_email(cls, value: str):
        return value.lower()

    @validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value is None:
            return value

        assert value <= date.today()
        return value

    @validator("password")
    def validate_password(cls, value):
        validate_password(value)
        return value


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmRegistrationBody(BaseModel):
    code: str


class LoginBody(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value: str):
        return value.lower()


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class ChangePasswordBody(BaseModel):
    old_password: str
    new_password: str


class ForgotPasswordBody(BaseModel):
    email: EmailStr


class ResetPasswordBody(BaseModel):
    code: str
    password: str
