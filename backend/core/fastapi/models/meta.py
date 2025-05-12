from pydantic import BaseModel, Field
from typing import Optional

class MetaModel(BaseModel):
    current_page: Optional[int] = Field(default=1, ge=1, description="Current page number (must be >= 1)")
    per_page: Optional[int] = Field(default=10, ge=1, description="Number of items per page (must be >= 1)")
    total_items: Optional[int] = Field(default=0, ge=0, description="Total number of items (must be >= 0)")
    total_pages: Optional[int] = Field(default=0, ge=0, description="Total number of pages (must be >= 0)")
