from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi import FastAPI
from conf import settings

TORTOISE_CONFIG = {
    'connections': {'default': settings().DB_URL},
    'apps': {"models": {"models": ["models", "aerich.models"]}},
}


def connect_db(app: FastAPI):
    Tortoise.init_models(["models", "aerich.models"], "models")
    register_tortoise(app, config=TORTOISE_CONFIG, generate_schemas=settings().TEST)
