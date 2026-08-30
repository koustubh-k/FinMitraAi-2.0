from langchain_core.tools import tool
from duckduckgo_search import DDGS
from typing import List, Dict, Any

@tool
def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web for recent news or information.
    Use this when you need up-to-date information not found in the ingested documents.
    Args:
        query: The search query string.
        max_results: The maximum number of results to return.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        return [{"error": str(e)}]
