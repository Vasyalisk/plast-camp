from fastapi import APIRouter
import schemas.users

router = APIRouter(tags=["users"])


@router.get("/me", response_model=schemas.users.MeResponse)
async def me():
    from datetime import datetime
    return schemas.users.MeResponse(username="User", created_at=datetime.now(), is_registration_finished=True)
