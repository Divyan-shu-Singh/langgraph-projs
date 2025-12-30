from typing import Any
from langchain.agents import create_agent
from api.groq_models import llm_client

class Agent:
    def __init__(self, agent_name, sys_prompt, llm, response_format = None, tools = None):
        self.name = agent_name
        self.prompt = sys_prompt
        self.llm = llm
        self.tools = tools
        self.response_format = response_format
        
    def make_agent(self, ) -> Any:
        return create_agent(model = self.llm,
                            tools= self.tools,
                            system_prompt= self.prompt,
                            response_format= self.response_format)