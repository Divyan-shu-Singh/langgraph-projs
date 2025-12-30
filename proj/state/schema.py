from typing import TypedDict, List, Optional

class CopilotState(TypedDict):
    query: str

    plan: Optional[List[str]]
    retrieved_docs: Optional[List[str]]

    draft_answer: Optional[str]
    critiques: Optional[List[str]]

    confidence: Optional[float]
    retries: int

    final_answer: Optional[str]
    abstained: bool
