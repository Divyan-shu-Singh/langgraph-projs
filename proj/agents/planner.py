from utils.agent_init import Agent
from utils.models import PlannerOutput
from utils.prompts import PLANNER_PROMPT
from api.groq_models import llm_client
from state.schema import CopilotState
from langchain_core.messages import HumanMessage
from typing import Any



def planner_agent(state : CopilotState) -> Any:
    query = state['query']
    agent = Agent(agent_name= 'planner_agent', sys_prompt= PLANNER_PROMPT, llm = llm_client, response_format= PlannerOutput)
    planner = agent.make_agent()  
    resp = planner.invoke({"messages":HumanMessage(query)})
    