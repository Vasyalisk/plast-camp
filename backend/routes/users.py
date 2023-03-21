from fastapi import APIRouter
import schemas.users

router = APIRouter(tags=["users"])


@router.get("/me", response_model=schemas.users.MeResponse)
async def me():
    from datetime import datetime
    return schemas.users.MeResponse(
        id=1,
        email="user@example.com",
        first_name="First",
        last_name="Last",
        nickname="User",
        created_at=datetime.now(),
        is_email_verified=True,
        role="BASE",
    )
