from enum import Enum


class EmailType(str, Enum):
    REGISTRATION = "REGISTRATION"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"


async def send(email_type: EmailType, **kwargs):
    # TODO: implement
    pass
