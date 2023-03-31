from fastapi import HTTPException, Request

import typing as t
from core import errors


class BaseService:
    def __init__(self, request: t.Optional[Request] = None):
        self.request = request

    @classmethod
    def raise_400(cls, detail: t.Optional[str] = errors.BAD_REQUEST):
        raise HTTPException(status_code=400, detail=detail)

    @classmethod
    def raise_401(cls, detail: t.Optional[str] = errors.UNAUTHORIZED):
        raise HTTPException(status_code=401, detail=detail)

    @classmethod
    def raise_403(cls, detail: t.Optional[str] = errors.PERMISSION_DENIED):
        raise HTTPException(status_code=403, detail=detail)

    @classmethod
    def raise_404(cls, detail: t.Optional[str] = errors.NOT_FOUND):
        raise HTTPException(status_code=404, detail=detail)

    async def get(self, *args, **kwargs):
        pass

    async def post(self, *args, **kwargs):
        pass

    async def patch(self, *args, **kwargs):
        pass

    async def put(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass
