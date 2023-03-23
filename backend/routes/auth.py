from fastapi import APIRouter, Depends
import schemas.auth
import services.auth
from core import security

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=schemas.auth.RegisterResponse, status_code=201)
async def register(body: schemas.auth.RegisterBody):
    """
    Зареєструвати нового користувача використувуючи унікальний емейл

    Якщо користувач з обраним емейлом і без паролю вже існую у БД, то оновити його дані
    """
    return await services.auth.Register().post(body)


@router.patch("/register/confirm", status_code=204)
async def confirm_registration(body: schemas.auth.ConfirmRegistrationBody):
    """
    Підтвердити реєстрацію користувача використовуючи унікальний секретний код з емейлу
    """
    return await services.auth.ConfirmRegistration().patch(body)


@router.post("/login", response_model=schemas.auth.LoginResponse)
async def login(body: schemas.auth.LoginBody):
    """
    Залогінити існуючого користувача використовуючи емей і пароль
    """
    return await services.auth.Login().post(body)


@router.patch("/password/change", status_code=204)
async def change_password(body: schemas.auth.ChangePasswordBody, authorize: security.Authorize = Depends()):
    """
    Змінити пароль як залогінений користувач
    """
    return await services.auth.ChangePassword().patch(body=body, authorize=authorize)


@router.post("/password/reset/request", status_code=204)
async def forgot_password(body: schemas.auth.ForgotPasswordBody):
    """
    Послати секретний код для зміни паролю на емейл
    """
    return await services.auth.ForgotPassword().post(body)


@router.post("/password/reset", status_code=204)
async def reset_password(body: schemas.auth.ResetPasswordBody):
    """
    Підтвердити зміну пароля за допомогою секретного коду з емейлу
    """
    return await services.auth.ResetPassword().post(body)
