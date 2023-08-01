import asyncio

import asyncpg
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.log import logger

from conf import settings

TORTOISE_CONFIG = {
    'connections': {'default': settings().DB_URL},
    'apps': {"models": {"models": ["models", "aerich.models"]}},
}


async def check_connection(attempts=10, timeout=1):
    async def _check_once():
        try:
            conn = await asyncpg.connect(settings().DB_URL)
        except Exception:
            return False

        await conn.close()
        return True

    for _ in range(attempts):
        is_connected = await _check_once()

        if is_connected:
            break

        logger.info("Connection attempt to DB failed, retrying...")
        await asyncio.sleep(timeout)


def connect_db(app: FastAPI):
    Tortoise.init_models(["models", "aerich.models"], "models")
    app.on_event("startup")(check_connection)
    register_tortoise(app, config=TORTOISE_CONFIG, generate_schemas=settings().TEST)
