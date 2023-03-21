from fastapi import APIRouter
import schemas.auth
import services.auth

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=schemas.auth.RegisterResponse)
async def register(body: schemas.auth.RegisterBody):
    """
    Зареєструвати нового користувача використувуючи унікальний емейл

    Якщо користувач з обраним емейлом і без паролю вже існую у БД, то оновити його дані
    """
    return await services.auth.register(body)


@router.post("/register/confirm", status_code=204)
async def confirm_registration(body: schemas.auth.ConfirmRegistrationBody):
    """
    Підтвердити реєстрацію користувача використовуючи унікальний секретний код з емейлу
    """
    return


@router.post("/login", response_model=schemas.auth.LoginResponse)
async def login(body: schemas.auth.LoginBody):
    """
    Залогінити існуючого користувача використовуючи емей і пароль
    """
    return schemas.auth.LoginResponse(access_token="abcd", refresh_token="efgh")


@router.post("/password/change", status_code=204)
async def change_password(body: schemas.auth.ChangePasswordBody):
    """
    Змінити пароль як залогінений користувач
    """
    return


@router.post("/password/reset/request", status_code=204)
async def forgot_password(body: schemas.auth.ForgotPasswordBody):
    """
    Послати секретний код для зміни паролю на емейл
    """
    return


@router.post("/password/reset", status_code=204)
async def reset_password(body: schemas.auth.ResetPasswordBody):
    """
    Підтвердити зміну пароля за допомогою секретного коду з емейлу
    """
    return
