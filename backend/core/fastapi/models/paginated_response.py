from core.fastapi.models.meta import MetaModel
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List, Dict, Any

class PaginatedResponse(BaseModel):
    data: List[Dict[str, Any]] = Field(default=[], description="The list of items for the current page")
    metadata: MetaModel = Field(..., description="Pagination metadata")
