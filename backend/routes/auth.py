from fastapi import APIRouter
import schemas.auth

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=schemas.auth.RegisterResponse)
async def register(body: schemas.auth.RegisterBody):
    """
    Register new user using unique email address
    """
    return schemas.auth.RegisterResponse(access_token="abcd", refresh_token="efgh")


@router.post("/register/confirm", status_code=204)
async def confirm_registration(body: schemas.auth.ConfirmRegistrationBody):
    """
    Confirm registration of the existing user using secret email code
    """
    return


@router.post("/login", response_model=schemas.auth.LoginResponse)
async def login(body: schemas.auth.LoginBody):
    """
    Login existing user using email and password
    """
    return schemas.auth.LoginResponse(access_token="abcd", refresh_token="efgh")


@router.post("/password/change", status_code=204)
async def change_password(body: schemas.auth.ChangePasswordBody):
    """
    Change password as logged user
    """
    return


@router.post("/password/reset/request", status_code=204)
async def forgot_password(body: schemas.auth.ForgotPasswordBody):
    """
    Request forget password email with secret code to specified email
    """
    return


@router.post("/password/reset", status_code=204)
async def reset_password(body: schemas.auth.ResetPasswordBody):
    """
    Reset password using secret code from email
    """
    return
