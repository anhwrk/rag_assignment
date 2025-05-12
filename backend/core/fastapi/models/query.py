from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional

class QueryModel(BaseModel):
    page: Optional[int] = Field(default=1, ge=1, description="Page number (must be >= 1)")
    per_page: Optional[int] = Field(default=10, ge=1, description="Number of items per page (must be >= 1)")
    sort_by: Optional[Dict[str, str]] = Field(default_factory=dict, description="Fields to sort by with order (e.g., {'name': 'asc'})")
    include: Optional[List[str]] = Field(default_factory=list, description="Fields to include in the response")
    filters: Optional[Dict[str, str]] = Field(default_factory=dict, description="Filters to apply to the query")

    @validator("sort_by", pre=True)
    def parse_sort_by(cls, value):
        """
        Parse sort_by from a string like 'name:asc,age:desc' into a dictionary.
        """
        if isinstance(value, str):
            sort_dict = {}
            for item in value.split(","):
                if ":" in item:
                    field, order = item.split(":")
                    if order not in {"asc", "desc"}:
                        raise ValueError("Invalid sort order. Must be 'asc' or 'desc'.")
                    sort_dict[field] = order
            return sort_dict
        return value
