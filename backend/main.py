from fastapi import FastAPI
from db import connect_db
from routes import include_routes
from core.security import configure_jwt
import exceptions

app = FastAPI(
    redoc_url=None,
    swagger_ui_parameters={"filter": True, "defaultModelsExpandDepth": -1},
)

exceptions.add_db_exception_handler(app)
connect_db(app)
configure_jwt(app)
include_routes(app)

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047
