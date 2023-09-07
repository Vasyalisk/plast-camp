from fastapi import APIRouter, Depends

import schemas.auth
import services.auth
from core import security

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=schemas.auth.RegisterResponse, status_code=201)
async def register(body: schemas.auth.RegisterBody):
    """
    Register new user using unique email

    If user with specified email and without password exists in DB - update user password
    """
    return await services.auth.Register().post(body)


@router.patch("/register/confirm", status_code=204)
async def confirm_registration(body: schemas.auth.ConfirmRegistrationBody):
    """
    Confirm registration using unique secret code from email
    """
    return await services.auth.ConfirmRegistration().patch(body)


@router.post("/login", response_model=schemas.auth.LoginResponse)
async def login(body: schemas.auth.LoginBody):
    """
    Login existing user using email and password
    """
    return await services.auth.Login().post(body)


@router.patch("/password/change", status_code=204)
async def change_password(body: schemas.auth.ChangePasswordBody, authorize: security.Authorize = Depends()):
    """
    Change password on logged in user
    """
    return await services.auth.ChangePassword().patch(body=body, authorize=authorize)


@router.post("/password/reset/request", status_code=204)
async def forgot_password(body: schemas.auth.ForgotPasswordBody):
    """
    Send secret code via email to reset password
    """
    return await services.auth.ForgotPassword().post(body)


@router.post("/password/reset", status_code=204)
async def reset_password(body: schemas.auth.ResetPasswordBody):
    """
    Reset password using secret code from email
    """
    return await services.auth.ResetPassword().post(body)
