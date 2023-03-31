import typing as t

from pydantic import BaseModel, conint
from pydantic.generics import GenericModel

from conf import settings

ResultType = t.TypeVar("ResultType")


class PaginatedQuery(BaseModel):
    page: t.Optional[conint(gt=0)] = 1
    page_size: t.Optional[conint(gt=0, le=settings().MAX_PAGE_SIZE)] = settings().DEFAULT_PAGE_SIZE

    def page_fields(self) -> t.Dict:
        return {"page": self.page, "page_size": self.page_size}

    def query_fields(
            self,
            *,
            include=None,
            exclude=None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> t.Dict:
        if exclude is None:
            exclude = set()

        exclude = {*exclude}
        exclude.add("page")
        exclude.add("page_size")

        return self.dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )


class PaginatedResponse(GenericModel, t.Generic[ResultType]):
    page: int
    page_size: int

    total_pages: int
    total_count: int

    results: t.List[ResultType]

    @classmethod
    def get_result_type(cls) -> t.Type[ResultType]:
        return cls.__fields__["results"].type_
