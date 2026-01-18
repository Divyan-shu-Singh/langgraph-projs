from proj.utils.models import PlannerOutput
from proj.utils.prompts import PLANNER_PROMPT
from proj.api.groq_models import llm_client
from proj.state.schema import CopilotState
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any

def planner_node(state: CopilotState) -> Dict[str, Any]:
    """
    Planner agent node - generates a plan from the user query.
    """
    query = state['query']
    
    structured_llm = llm_client.with_structured_output(PlannerOutput)
    
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=query)
    ]
    
    response = structured_llm.invoke(messages)
    
    return {
        "plan": response["plan"]
    }