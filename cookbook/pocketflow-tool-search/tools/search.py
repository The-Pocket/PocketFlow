import os
from serpapi import GoogleSearch
from typing import Dict, List, Optional

class SearchTool:
    """Tool for performing web searches using SerpAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize search tool with API key
        
        Args:
            api_key (str, optional): SerpAPI key. Defaults to env var SERPAPI_API_KEY.
        """
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpAPI key not found. Set SERPAPI_API_KEY env var.")
            
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform Google search via SerpAPI
        
        Args:
            query (str): Search query
            num_results (int, optional): Number of results to return. Defaults to 5.
            
        Returns:
            List[Dict]: Search results with title, snippet, and link
        """
        # Configure search parameters
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        
        try:
            # Execute search
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract organic results
            if "organic_results" not in results:
                return []
                
            processed_results = []
            for result in results["organic_results"][:num_results]:
                processed_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
                
            return processed_results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
