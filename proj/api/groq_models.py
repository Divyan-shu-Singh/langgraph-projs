from langchain_groq import ChatGroq
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


llm_client = ChatGroq(
    api_key= os.getenv('GROQ_API_KEY'), # type: ignore
    model="meta-llama/llama-4-scout-17b-16e-instruct", 
    temperature=0.6
)
