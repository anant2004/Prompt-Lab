from pydantic import BaseModel, Field, field_validator
from typing import List
import re

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=10, max_length=3000)
    @field_validator('prompt')
    @classmethod

    def sanitize_prompt(cls, v: str) -> str:
        v = v.strip()
        if v.count("{") > 5 or v.count("}") > 5:
            raise ValueError("Prompt contains suspicious patterns")
        
        v = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", v)
        return v
    
class ScoreBreakdown(BaseModel):
    clarity: int = Field(ge=0, le=100)
    context: int = Field(ge=0, le=100)
    specificity: int = Field(ge=0, le=100)
    structure: int = Field(ge=0, le=100)
    tone: int = Field(ge=0, le=100)

class EvaluationResponse(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    scores: ScoreBreakdown
    strengths: List[str] = Field(max_length=5)
    weaknesses: List[str] = Field(max_length=5)
    suggestions: List[str] = Field(max_length=5)
    improved_prompt: str = Field(max_length=2000)