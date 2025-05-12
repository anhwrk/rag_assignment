from typing import List
from pydantic import BaseModel, Field

class BraFitting(BaseModel):
    description: str = Field(..., description="The description of the bra fitting issue.")
    recommendation: str = Field(..., description="The recommendation for the user.")
    reasoning: str = Field(..., description="The reasoning for the recommendation.")
    common_issues: List[str] = Field(..., description="The common issues for the recommendation.")
    fit_tips: str = Field(..., description="The fit tips for the recommendation.")
