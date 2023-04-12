from datetime import datetime

import pydantic


class CountryResponse(pydantic.BaseModel):
    id: int
    created_at: datetime

    name_ukr: str
    name_orig: str

    class Config:
        orm_mode = True
