"""Third-party data source related node classes."""

import json
import logging
from datetime import date
from pocketflow import Node
from utils import search, ai
from utils.generators.third_party_analysis import generate_tavily_query_prompt, generate_analysis_prompt

class DecideTavilyQueries(Node):
    """Uses AI to generate search queries for third-party sources based on lead and company info."""
    def prep(self, shared):
        """Prepare context for AI to generate search queries."""
        company_name = shared.get('company_name', '')
        lead_first_name = shared.get('lead_first_name', '')
        lead_last_name = shared.get('lead_last_name', '')
        
        if not company_name and not lead_first_name and not lead_last_name:
            logging.warning("Missing lead name and company name for query generation")
            return None
            
        # Get additional context if available
        website_report = shared.get('website_report', '')
        linkedin_report = shared.get('linkedin_report', '')
        
        # Create a context dict
        context = {
            'company_name': company_name,
            'lead_first_name': lead_first_name,
            'lead_last_name': lead_last_name,
            'has_website_data': bool(website_report),
            'has_linkedin_data': bool(linkedin_report)
        }
        
        logging.info(f"Preparing context for query generation: {context}")
        return context
    
    def exec(self, context):
        """Generate search queries using LLM."""
        if not context:
            return json.dumps({"error": "Insufficient context for query generation"})
            
        company_name = context.get('company_name', '')
        lead_first_name = context.get('lead_first_name', '')
        lead_last_name = context.get('lead_last_name', '')
        
        # Craft prompt for AI using the generator
        prompt = generate_tavily_query_prompt(lead_first_name=lead_first_name, lead_last_name=lead_last_name, company_name=company_name)
        
        try:
            response = ai.call_llm(prompt)
            
            # Extract JSON from response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
                
            # Validate and return queries
            queries = json.loads(json_str)
            
            # Ensure it's a list of strings
            if not isinstance(queries, list):
                raise ValueError("Response is not a list")
                
            # Filter out any non-string items
            queries = [q for q in queries if isinstance(q, str)]
            
            if not queries:
                raise ValueError("No valid queries generated")
                
            logging.info(f"Generated {len(queries)} search queries")
            return json.dumps(queries)
            
        except Exception as e:
            logging.error(f"Error generating search queries: {str(e)}")
            return json.dumps({"error": f"Failed to generate queries: {str(e)}"})
    
    def post(self, shared, prep_res, exec_res):
        """Store generated queries in shared."""
        try:
            queries = json.loads(exec_res)
            
            # Check if there was an error
            if isinstance(queries, dict) and "error" in queries:
                logging.warning(f"Query generation error: {queries['error']}")
                shared['tavily_queries'] = []
                return "search_failed"
                
            # Store queries
            shared['tavily_queries'] = queries
            logging.info(f"Stored {len(queries)} search queries")
            return "default"
            
        except Exception as e:
            logging.error(f"Error processing generated queries: {str(e)}")
            shared['tavily_queries'] = []
            return "search_failed"


class SearchThirdPartySources(Node):
    """Searches third-party sources for additional information on the lead/company."""
    def prep(self, shared):
        """Get search queries from AI generation."""
        tavily_queries = shared.get('tavily_queries', [])
        
        if not tavily_queries:
            logging.warning("No search queries available for third-party search")
            return None
            
        logging.info(f"Preparing to search with {len(tavily_queries)} queries")
        return tavily_queries
    
    def exec(self, queries):
        """Execute searches for each query."""
        if not queries:
            return []
            
        all_results = []
        seen_urls = set()  # Track URLs to avoid duplicates
        
        for query in queries:
            try:
                logging.info(f"Searching with query: {query}")
                results = search.web_search(query, max_results=3)
                
                # Add only new results (avoid duplicate URLs)
                for result in results:
                    url = result.get('url')
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append(result)
                        
            except Exception as e:
                logging.error(f"Error searching for query '{query}': {str(e)}")
                continue
                
        logging.info(f"Found {len(all_results)} unique search results across all queries")
        return all_results
        
    def post(self, shared, prep_res, exec_res):
        """Store search results (raw and processed) in shared."""
        if not exec_res:
            logging.warning("No third-party search results found")
            shared['raw_third_party_search_results'] = [] # Store empty list
            shared['third_party_sources'] = []
            return "no_results"
            
        shared['raw_third_party_search_results'] = exec_res # Store raw results
        shared['third_party_sources'] = exec_res # Keep original key
        logging.info(f"Stored {len(exec_res)} third-party search results (raw and processed)")
        return "default"


class AnalyzeThirdPartySources(Node):
    """Analyzes third-party source results to extract relevant intelligence."""
    def prep(self, shared):
        """Prepare third-party sources and context for analysis."""
        sources = shared.get('third_party_sources', [])
        company_name = shared.get('company_name', '')
        lead_first_name = shared.get('lead_first_name', '')
        lead_last_name = shared.get('lead_last_name', '')
        
        if not sources:
            logging.warning("No third-party sources to analyze")
            return None
            
        # Create a context object with all relevant information
        context = {
            'sources': sources,
            'company_name': company_name,
            'lead_first_name': lead_first_name,
            'lead_last_name': lead_last_name
        }
        
        logging.info(f"Preparing {len(sources)} sources for analysis")
        return context
        
    def exec(self, context):
        """Generate precision intelligence report from third-party sources."""
        if not context or not context.get('sources'):
            return "No third-party data to analyze."
            
        sources = context['sources']
        company_name = context['company_name']
        lead_first_name = context['lead_first_name']
        lead_last_name = context['lead_last_name']
        current_date_today = date.today()
            
        # Craft the analysis prompt using the generator, passing the date
        analysis_prompt = generate_analysis_prompt(
            lead_first_name=lead_first_name, 
            lead_last_name=lead_last_name,
            company_name=company_name, 
            sources=sources,
            current_date=current_date_today
        )
        
        try:
            logging.info("Calling LLM to generate third-party analysis report")
            precision_report = ai.call_llm(analysis_prompt)
            return precision_report
        except Exception as e:
            logging.error(f"Error generating third-party analysis: {str(e)}")
            return f"Error analyzing third-party sources: {str(e)}"
    
    def post(self, shared, prep_res, exec_res):
        """Store the precision intelligence report in shared."""
        if not exec_res or exec_res.startswith("Error"):
            logging.warning(f"Third-party analysis failed: {exec_res}")
            shared['precision_intelligence_report'] = f"Analysis failed: {exec_res}"
        else:
            logging.info("Successfully generated precision intelligence report")
            shared['precision_intelligence_report'] = exec_res
            
        return "default"  # Continue flow regardless 