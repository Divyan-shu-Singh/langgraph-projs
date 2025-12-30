from pydantic import BaseModel
from typing import Optional, Literal

class PlannerOutput(BaseModel):
    action: Literal["search", "retrieve", "sql", "answer"]
    reasoning: str
    query: Optional[str]

class RetrieverOutput(BaseModel):
    