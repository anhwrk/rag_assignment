from pydantic import BaseModel, Field, validator

class RecommendationDTO(BaseModel):
    text: str = Field(..., description="The user query for the recommendation.")
    
    @validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        cleaned_text = v.strip()
        
        if not cleaned_text:
            raise ValueError("Text cannot be empty")
            
        if len(cleaned_text) < 10:
            raise ValueError("Please provide more details about your measurements and fit issues")
            
        if len(cleaned_text) > 500:
            raise ValueError("Query is too long, please be more concise")
            
        # Check if contains numbers (likely measurements)
        if not any(char.isdigit() for char in cleaned_text):
            raise ValueError("Please include your measurements (bust and underbust)")
            
        return cleaned_text
