"""Utility function for performing web searches using Tavily API."""

import os
import logging
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Tavily client
tavily_api_key = os.environ.get("TAVILY_API_KEY")
tavily_client: TavilyClient | None = None
if tavily_api_key:
    try:
        tavily_client = TavilyClient(api_key=tavily_api_key)
        logging.info("Tavily client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Tavily client: {e}")
        tavily_client = None
else:
    logging.warning("TAVILY_API_KEY not found in environment variables. Search utility will not function.")

def call_tavily_search(query: str, max_results: int = 3) -> list[dict]:
    """
    Performs a web search using the Tavily Search API.

    Args:
        query: The search query string.
        max_results: The maximum number of search results to return.

    Returns:
        A list of search result dictionaries (e.g., {'title': ..., 'url': ..., 'content': ...}),
        or an empty list if an error occurs or no results are found.
    """
    if not tavily_client:
        logging.error("Tavily client not initialized. Cannot perform search.")
        return [] # Return empty list on failure

    logging.info(f"Performing Tavily search for query: \"{query}\" (max_results={max_results})")
    try:
        # Use the basic search endpoint
        response = tavily_client.search(
            query=query,
            search_depth="basic", # basic is often sufficient, use 'advanced' if needed
            max_results=max_results,
            include_answer=False, # We don't need Tavily's generated answer
            include_raw_content=False # Raw content not needed for this use case
        )
        
        results = response.get('results', [])
        logging.info(f"Tavily search returned {len(results)} results for query \"{query}\".")
        return results
        
    except Exception as e:
        logging.error(f"Error during Tavily search for query \"{query}\": {e}", exc_info=True)
        return [] # Return empty list on error

if __name__ == '__main__':
    # Example usage for testing - Requires .env file with TAVILY_API_KEY
    print("\n--- Testing Tavily Search Utility --- (Requires .env)")
    
    if not tavily_client:
        print("Skipping test: Tavily client not initialized.")
    else:
        test_query = "OpenAI review site:g2.com"
        search_results = call_tavily_search(test_query, max_results=2)
        
        print(f"\n--- Tavily Search Results for '{test_query}' ---")
        if search_results:
            import json
            print(json.dumps(search_results, indent=2))
        else:
            print("No results returned or an error occurred.")
        print("-------------------------------------------") 