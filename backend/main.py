from fastapi import FastAPI
from db import start_db
from routes import include_routes

app = FastAPI(
    redoc_url=None,
    swagger_ui_parameters={"filter": True, "defaultModelsExpandDepth": -1},
)

start_db(app)
include_routes(app)

# For swagger tutorials: https://fastapi.tiangolo.com/advanced/sub-applications/
# https://github.com/tiangolo/fastapi/issues/3047