from proj.state.schema import CopilotState
from typing import Dict, Any
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from proj.api.groq_models import llm_client


def web_search_node(state: CopilotState) -> Dict[str, Any]:
    """Search web using Tavily API."""
    query = state["query"]
    
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general",
    )
    
    llm_with_tool = llm_client.bind_tools([tavily_search_tool])
    
    web_results = llm_with_tool.invoke({"messgaes":query})   

    return {"web_search_results": web_results}


def retrieval_node(state: CopilotState) -> Dict[str, Any]:
    """Retrieve documents from vector database."""
    query = state["query"]
    
    # Your vector DB retrieval logic here
    # retrieved_docs = vector_db.similarity_search(query, k=5)
    
    # Placeholder
    retrieved_docs = [
        "Doc 1: Retrieved from knowledge base...",
        "Doc 2: More relevant information..."
    ]
    
    return {"retrieved_docs": retrieved_docs}