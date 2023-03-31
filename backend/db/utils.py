from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from conf import settings

TORTOISE_CONFIG = {
    'connections': {'default': settings().DB_URL},
    'apps': {"models": {"models": ["models", "aerich.models"]}},
}


def connect_db(app: FastAPI):
    Tortoise.init_models(["models", "aerich.models"], "models")
    register_tortoise(app, config=TORTOISE_CONFIG, generate_schemas=settings().TEST)
