from pydantic import BaseModel, Field, validator

class RecommendationDTO(BaseModel):
    text: str = Field(..., description="The user query for the recommendation.")
    
    @validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()
