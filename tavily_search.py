from dotenv import load_dotenv
import os
from langchain_community.tools import TavilySearchResults

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

def tavily_search(query):
    
    tool = TavilySearchResults(
        max_results=5,
        response_format = 'content_and_artifact'
    )
    response = tool.invoke(query)

    #context = crawling(response)

    return response