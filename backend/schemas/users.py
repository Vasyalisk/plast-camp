from pydantic import BaseModel
from datetime import datetime


class MeResponse(BaseModel):
    username: str
    created_at: datetime
    is_registration_finished: bool
