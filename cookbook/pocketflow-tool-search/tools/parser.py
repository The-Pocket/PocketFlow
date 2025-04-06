from typing import Dict, List
from utils.call_llm import call_llm

def analyze_results(query: str, results: List[Dict]) -> Dict:
    """Analyze search results using LLM
    
    Args:
        query (str): Original search query
        results (List[Dict]): Search results to analyze
        
    Returns:
        Dict: Analysis including summary and key points
    """
    # Format results for prompt
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append(f"""
Result {i}:
Title: {result['title']}
Snippet: {result['snippet']}
URL: {result['link']}
""")
    
    prompt = f"""
Analyze these search results for the query: "{query}"

{'\n'.join(formatted_results)}

Please provide:
1. A concise summary of the findings (2-3 sentences)
2. Key points or facts (up to 5 bullet points)
3. Suggested follow-up queries (2-3)

Output in YAML format:
```yaml
summary: >
    brief summary here
key_points:
    - point 1
    - point 2
follow_up_queries:
    - query 1
    - query 2
```
"""
    
    try:
        response = call_llm(prompt)
        # Extract YAML between code fences
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        
        import yaml
        analysis = yaml.safe_load(yaml_str)
        
        # Validate required fields
        assert "summary" in analysis
        assert "key_points" in analysis
        assert "follow_up_queries" in analysis
        assert isinstance(analysis["key_points"], list)
        assert isinstance(analysis["follow_up_queries"], list)
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing results: {str(e)}")
        return {
            "summary": "Error analyzing results",
            "key_points": [],
            "follow_up_queries": []
        }