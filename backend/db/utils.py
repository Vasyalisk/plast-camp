from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from conf import settings

TORTOISE_CONFIG = {
    'connections': {'default': settings().DB_URL},
    'apps': {"models": {"models": ["models", "aerich.models"]}},
}


def connect_db(app: FastAPI):
    register_tortoise(app, config=TORTOISE_CONFIG)
