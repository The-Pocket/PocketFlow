from pocketflow import Node
from tools.search import SearchTool
from tools.parser import analyze_results
from typing import List, Dict

class SearchNode(Node):
    """Node to perform web search using SerpAPI"""
    
    def prep(self, shared):
        return shared.get("query"), shared.get("num_results", 5)
        
    def exec(self, inputs):
        query, num_results = inputs
        if not query:
            return []
            
        searcher = SearchTool()
        return searcher.search(query, num_results)
        
    def post(self, shared, prep_res, exec_res):
        shared["search_results"] = exec_res
        return "default"

class AnalyzeResultsNode(Node):
    """Node to analyze search results using LLM"""
    
    def prep(self, shared):
        return shared.get("query"), shared.get("search_results", [])
        
    def exec(self, inputs):
        query, results = inputs
        if not results:
            return {
                "summary": "No search results to analyze",
                "key_points": [],
                "follow_up_queries": []
            }
            
        return analyze_results(query, results)
        
    def post(self, shared, prep_res, exec_res):
        shared["analysis"] = exec_res
        
        # Print analysis
        print("\nSearch Analysis:")
        print("\nSummary:", exec_res["summary"])
        
        print("\nKey Points:")
        for point in exec_res["key_points"]:
            print(f"- {point}")
            
        print("\nSuggested Follow-up Queries:")
        for query in exec_res["follow_up_queries"]:
            print(f"- {query}")
            
        return "default"
