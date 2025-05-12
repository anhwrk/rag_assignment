from core.utils import make_optional
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Type
from datetime import datetime

class RecommendationDTO(BaseModel):
    text: str = Field(..., description="The user query for the recommendation.")
