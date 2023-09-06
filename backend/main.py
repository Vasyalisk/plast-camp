import logging
import os

from fastapi import FastAPI, Security
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import db
import exceptions
from admin import mount_admin
from conf import settings
from core import redis, security
from routes import include_routes
from schemas import init_schemas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=settings().LOG_LEVEL)
app = FastAPI(
    redoc_url=None,
    swagger_ui_parameters={
        "filter": True,
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True
    },
    dependencies=[
        Security(security.AuthorizationHeader)
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings().ALLOWED_HOSTS
)

init_schemas()
exceptions.add_db_exception_handler(app)
db.connect_db(app)
security.configure_jwt(app)
include_routes(app)
mount_admin(app)


@app.on_event("shutdown")
async def on_shutdown():
    await redis.close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
