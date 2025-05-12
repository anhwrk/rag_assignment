from pydantic import BaseModel
from typing import List, Optional

class RecommendationResponse(BaseModel):
    recommendation: str
    confidence: float
    reasoning: str
    fit_tips: str
    identified_issues: Optional[List[str]]
    
