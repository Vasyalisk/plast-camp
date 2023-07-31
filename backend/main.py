from fastapi import FastAPI, Security
from starlette.middleware.cors import CORSMiddleware

import db
import exceptions
from admin.app import admin_app
from core import redis, security
from routes import include_routes
from schemas import init_schemas

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
app.mount("/admin", admin_app, name="admin")


@app.on_event("startup")
async def on_startup():
    await admin_app.configure()


@app.on_event("shutdown")
async def on_shutdown():
    await redis.close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
