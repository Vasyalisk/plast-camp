from pydantic import BaseModel, EmailStr


class RegisterBody(BaseModel):
    email: EmailStr
    password: str
    username: str


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmRegistrationBody(BaseModel):
    code: str


class LoginBody(BaseModel):
    email: str
    password: str


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
