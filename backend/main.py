import logging
import os

from fastapi import FastAPI, Security
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import db
import exceptions
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

init_schemas()
exceptions.add_db_exception_handler(app)
db.connect_db(app)
security.configure_jwt(app)
include_routes(app)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.on_event("shutdown")
async def on_shutdown():
    await redis.close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
