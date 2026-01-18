from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Annotated
from enum import Enum

class PlannerOutput(BaseModel):
    plan: List[str] = Field(description="List of steps to answer the query")

class ValidationOutput(BaseModel):
    can_handle: bool = Field(description="Whether the query can be handled")
    reasoning: str = Field(description="Explanation of the decision")
    suggestion: Optional[str] = Field(
        default=None, 
        description="Message for user if query cannot be handled"
    )

class ActionType(str, Enum):
    RETRIEVAL = "retrieval"
    WEB_SEARCH = "web_search"
    BOTH = "both"

class ActionDecisionOutput(BaseModel):
    actions: List[ActionType] = Field(description="List of actions needed to execute the plan")
    reasoning: str = Field(description="Why these actions were chosen")