from core.fastapi.models import QueryModel, PrismaQueryModel, MetaModel
from pydantic import BaseModel

class GetQueries(BaseModel):
    query: QueryModel
    prisma_query: PrismaQueryModel
    metadata: MetaModel
