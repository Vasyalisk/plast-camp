import typing as t

from fastapi import HTTPException, Request

from core import errors


class BaseService:
    class HttpException400(HTTPException):
        """
        Bad request exception
        """
        def __init__(self, detail: t.Optional[str] = errors.BAD_REQUEST):
            super().__init__(status_code=400, detail=detail)

    class HttpException401(HTTPException):
        """
        Unauthorized exception
        """
        def __init__(self, detail: t.Optional[str] = errors.UNAUTHORIZED):
            super().__init__(status_code=401, detail=detail)

    class HttpException403(HTTPException):
        """
        Permission denied / forbidden exception
        """
        def __init__(self, detail: t.Optional[str] = errors.PERMISSION_DENIED):
            super().__init__(status_code=403, detail=detail)

    class HttpException404(HTTPException):
        """
        Not found exception
        """
        def __init__(self, detail: t.Optional[str] = errors.NOT_FOUND):
            super().__init__(status_code=404, detail=detail)

    def __init__(self, request: t.Optional[Request] = None):
        self.request = request

    async def get(self, *args, **kwargs) -> t.Any:
        raise NotImplementedError()

    async def post(self, *args, **kwargs) -> t.Any:
        raise NotImplementedError()

    async def patch(self, *args, **kwargs) -> t.Any:
        raise NotImplementedError()

    async def put(self, *args, **kwargs) -> t.Any:
        raise NotImplementedError()

    async def delete(self, *args, **kwargs) -> t.Any:
        raise NotImplementedError()
