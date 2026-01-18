from proj.utils.models import ActionDecisionOutput
from proj.utils.prompts import ACTION_DECISION_PROMPT
from proj.api.groq_models import llm_client
from proj.state.schema import CopilotState
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any

def action_decision_node(state: CopilotState) -> Dict[str, Any]:
    """Decide which actions (retrieval/web_search/both) to take."""
    
    structured_llm = llm_client.with_structured_output(ActionDecisionOutput)
    
    prompt = ACTION_DECISION_PROMPT.format(
        query=state["query"],
        plan=state.get("plan", [])
    )
    
    response = structured_llm.invoke([SystemMessage(content=prompt)])
    
    actions = [action.value for action in response["actions"]]
    
    return {"action": actions}