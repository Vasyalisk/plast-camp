from pydantic.generics import GenericModel
from pydantic import BaseModel, conint
import typing as t
from conf import settings

ResultType = t.TypeVar("ResultType")


class PaginatedQuery(BaseModel):
    page: t.Optional[conint(gt=0)] = 1
    page_size: t.Optional[conint(gt=0, le=settings().MAX_PAGE_SIZE)] = settings().DEFAULT_PAGE_SIZE

    def page_fields(self) -> dict:
        return {"page": self.page, "page_size": self.page_size}


class PaginatedResponse(GenericModel, t.Generic[ResultType]):
    page: int
    page_size: int

    total_pages: int
    total_count: int

    results: t.List[ResultType]
