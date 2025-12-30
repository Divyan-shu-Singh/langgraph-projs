from langchain_groq import ChatGroq
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from dotenv import load_dotenv

# load_dotenv('../../.env')

llm_client = ChatGroq(
    api_key= os.getenv('GROQ_API_KEY'), # type: ignore
    model="qwen/qwen3-32b", 
    temperature=0.6
)

embed_client = GoogleGenerativeAIEmbeddings(
    api_key= os.getenv("GOOGLE_API_KEY")
    model="models/gemini-embedding-001"
) # type: ignore