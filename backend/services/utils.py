import typing as t

import models
import schemas.pagination

ResponseModel = t.TypeVar("ResponseModel", bound=schemas.pagination.PaginatedResponse)


def paginate_queryset(queryset: models.QuerySet, paginated_query: schemas.pagination.PaginatedQuery) -> models.QuerySet:
    """
    Paginate query according to provided schemas.pagination.PaginatedQuery instance (or instance of subclass)
    :param queryset:
    :param paginated_query:
    :return: paginated queryset
    """
    offset = (paginated_query.page - 1) * paginated_query.page_size
    return queryset.offset(offset).limit(paginated_query.page_size)


async def paginate_response(
        queryset: models.QuerySet,
        request_query: schemas.pagination.PaginatedQuery,
        response_model: t.Type[schemas.pagination.PaginatedResponse],
) -> ResponseModel:
    """
    Return standardized paginated response
    :param queryset:
    :param request_query:
    :param response_model:
    :return:
    """
    total_count = await queryset.count()
    total_pages = total_count // request_query.page_size

    if total_count % request_query.page_size:
        total_pages += 1

    results = [
        response_model.get_result_type().from_orm(one)
        for one in await paginate_queryset(queryset, request_query)
    ]
    return response_model(
        results=results,
        total_count=total_count,
        total_pages=total_pages,
        **request_query.page_fields(),
    )
