from core.fastapi.models import QueryModel, PrismaQueryModel, MetaModel, GetQueries
from fastapi import Request
from typing import Dict, TypeVar
from loguru import logger

T = TypeVar("T")

async def get_queries(request: Request) -> GetQueries:
    query = QueryModel(
        page=int(request.query_params.get("page", 1)),
        per_page=int(request.query_params.get("per_page", 10)),
        sort_by=request.query_params.get("sort_by"),
        include=request.query_params.getlist("include"),
        filters={key: value for key, value in request.query_params.items() if key.startswith("filter_")},
    )

    prisma_query = PrismaQueryModel(
        skip=(query.page - 1) * query.per_page if query.per_page > 0 else None,
        take=query.per_page if query.per_page > 0 else None,
        order=query.sort_by if query.sort_by else None,
        where=query.filters if query.filters else None,
        include={key: True for key in query.include} if query.include else None,
    )

    metadata = MetaModel(
        current_page=query.page,
        per_page=query.per_page,
        total_items=None,
        total_pages=None,
    )

    return GetQueries(
        query=query,
        prisma_query=prisma_query,
        metadata=metadata,
    )

async def get_params(request: Request) -> Dict[str, str]:
    return request.path_params or {}


async def get_body(request: Request) -> T:
    try:
        return await request.json()
    except Exception:
        return {}
