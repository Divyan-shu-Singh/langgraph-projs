from proj.utils.models import ValidationOutput 
from proj.utils.prompts import CAPABILITY_VALIDATOR_PROMPT
from proj.api.groq_models import llm_client
from proj.state.schema import CopilotState
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any

def validator_node(state: CopilotState) -> Dict[str, Any]:
    """
    Validates if query can be handled by current capabilities.
    """
    structured_llm = llm_client.with_structured_output(ValidationOutput)
    
    prompt_content = CAPABILITY_VALIDATOR_PROMPT.format(
        query=state["query"],
        plan=state.get("plan", [])
    )
    
    response = structured_llm.invoke([
        SystemMessage(content=prompt_content)
    ])
    
    if not response["can_handle"]:
        return {
            "abstained": True,
            "final_answer": response["suggestion"],
            "confidence": 0.0
        }
    
    return {} 