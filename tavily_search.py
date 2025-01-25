from langchain_community.tools import TavilySearchResults

def tavily_search(query):
    
    tool = TavilySearchResults(
        max_results=5,
        response_format = 'content_and_artifact'
    )
    response = tool.invoke(query)

    #context = crawling(response)

    return response