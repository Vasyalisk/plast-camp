from fastapi import FastAPI, Security
import db
from routes import include_routes
from core import security, redis
import exceptions

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

exceptions.add_db_exception_handler(app)
db.connect_db(app)
security.configure_jwt(app)
include_routes(app)


@app.on_event("shutdown")
async def on_shutdown():
    await redis.close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
