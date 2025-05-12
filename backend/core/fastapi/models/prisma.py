from pydantic import BaseModel, Field
from typing import Dict, Optional

class PrismaQueryModel(BaseModel):
    skip: Optional[int] = Field(default=None, ge=0, description="Number of records to skip")
    take: Optional[int] = Field(default=None, gt=0, description="Number of records to take")
    order: Optional[Dict[str, str]] = Field(default=None, description="Order by conditions (e.g., {'field': 'asc'})")
    where: Optional[Dict[str, str]] = Field(default=None, description="Filtering conditions (e.g., {'field': 'value'})")
    include: Optional[Dict[str, bool]] = Field(default=None, description="Relations to include (e.g., {'relation': True})")
