from fastapi import FastAPI, Security
from admin.app import app as admin_app
from admin.providers import EmailPasswordProvider

import db
import exceptions
from core import redis, security
from routes import include_routes
from schemas import init_schemas
import models

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

init_schemas()
exceptions.add_db_exception_handler(app)
db.connect_db(app)
security.configure_jwt(app)
include_routes(app)

login_provider = EmailPasswordProvider(
    admin_model=models.User,  # type: ignore
    login_logo_url="https://preview.tabler.io/static/logo.svg"
)

app.mount("/admin", admin_app, name="admin")


@app.on_event("startup")
async def on_startup():
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        # template_folders=[os.path.join(BASE_DIR, "templates")],
        providers=[login_provider],
        redis=redis.connection,
    )


@app.on_event("shutdown")
async def on_shutdown():
    await redis.close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
