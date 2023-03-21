from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError


def add_db_exception_handler(app: FastAPI):
    app.exception_handler(IntegrityError)(_on_integrity_error)


async def _on_integrity_error(request: Request, err: IntegrityError):
    detail = str(err).split("\n")[-1].replace("DETAIL: ", "")
    return JSONResponse(status_code=400, content={"detail": detail})
