import models
import schemas.pagination
import typing as t

ResponseModel = t.TypeVar("ResponseModel", bound=schemas.pagination.PaginatedResponse)


def paginate_queryset(queryset: models.QuerySet, paginated_query: schemas.pagination.PaginatedQuery) -> models.QuerySet:
    offset = (paginated_query.page - 1) * paginated_query.page_size
    return queryset.offset(offset).limit(paginated_query.page_size)


async def paginate_response(
        queryset: models.QuerySet,
        request_query: schemas.pagination.PaginatedQuery,
        response_model: t.Type[schemas.pagination.PaginatedResponse],
) -> ResponseModel:
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
