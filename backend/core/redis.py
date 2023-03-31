# See issue with stubs https://github.com/redis/redis-py/issues/2249
# Plugin location https://www.jetbrains.com/help/pycharm/directories-used-by-the-ide-to-store-settings-caches-plugins-and-logs.html#301b9a53
import secrets
import typing as t
from enum import Enum

from fakeredis.aioredis import FakeRedis
from redis import asyncio as aioredis

from conf import settings


class CodeType(str, Enum):
    REGISTER = "REGISTER"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"


_redis_class = aioredis.Redis

if settings().TEST:
    _redis_class = FakeRedis

connection = _redis_class(
    host=settings().REDIS_HOST,
    port=settings().REDIS_PORT,
    password=settings().REDIS_PASSWORD,
    decode_responses=True,
    db=settings().REDIS_DB,
)


async def close_redis_connection():
    await connection.close()


async def _create_unique_code(code_type: CodeType) -> str:
    code = secrets.token_urlsafe(8)
    token = f"{code_type}:{code}"

    if await connection.exists(token):
        return await _create_unique_code(code_type)

    return code


async def generate_code(user_id, code_type: CodeType) -> str:
    code = await _create_unique_code(code_type)
    token = f"{code_type}:{code}"

    ex = None
    if code_type == CodeType.FORGOT_PASSWORD:
        ex = settings().RESET_CODE_EXPIRES

    await connection.set(token, user_id, ex=ex)
    return code


async def check_code(code, code_type: CodeType) -> t.Optional[str]:
    token = f"{code_type}:{code}"
    return await connection.get(token)


async def delete_code(code, code_type: CodeType):
    token = f"{code_type}:{code}"
    return await connection.delete(token)
