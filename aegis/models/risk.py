from pydantic import BaseModel, Field


class RiskOutput(BaseModel):
    score: float = Field(ge=0, le=1, description="Risk score from 0 (safe) to 1 (dangerous)")
    reasoning: str = Field(description="Brief explanation of the risk assessment")
