from fastapi import FastAPI
from db import connect_db
from routes import include_routes
from core.security import configure_jwt
from core.redis import close_redis_connection
import exceptions

app = FastAPI(
    redoc_url=None,
    swagger_ui_parameters={"filter": True, "defaultModelsExpandDepth": -1},
)

exceptions.add_db_exception_handler(app)
connect_db(app)
configure_jwt(app)
include_routes(app)


@app.on_event("shutdown")
async def on_shutdown():
    await close_redis_connection()

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
