"""Node definitions for the V1 lead processing workflow."""

import logging
import re # For basic URL validation

from pocketflow import Node

# Import placeholder utility functions
from utils import web_scraper, linkedin_scraper, ai_analyzer, ai_generator, database

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Node Definitions ---

class LoadLeadData(Node):
    """Loads the initial lead data passed into the flow run."""
    # exec method is no longer strictly needed as data is pre-loaded into shared
    # def exec(self, initial_params):
    #     """Simply passes the initial parameters through."""
    #     logging.info(f"Loading lead data: {initial_params.get('lead_name', 'N/A')}")
    #     return initial_params

    # prep is also not strictly needed if exec is removed, but can be kept simple
    def prep(self, shared):
        logging.info(f"Starting flow for lead: {shared.get('lead_name', 'N/A')}")
        return None # Nothing needed for exec
    
    # exec could be removed or simplified
    def exec(self, prep_res):
        return None # Nothing to compute

    def post(self, shared, prep_res, exec_res):
        """Initializes remaining placeholder keys in the shared store."""
        # Lead data is already in shared from main.py
        # Initialize keys that subsequent nodes expect, even if None, if not already present
        shared.setdefault('website_raw_content', None)
        shared.setdefault('website_report', None)
        shared.setdefault('linkedin_raw_profile', None)
        shared.setdefault('linkedin_report', None)
        shared.setdefault('email_subject', None)
        shared.setdefault('email_body', None)
        logging.info("Ensured shared store placeholders are initialized.")
        return "default" # Proceed to CheckWebsiteExists

class CheckWebsiteExists(Node):
    """Checks if a potentially valid website URL is provided."""
    def prep(self, shared):
        return shared.get("company_website")

    def exec(self, website_url):
        """Basic check if the URL is a non-empty string and starts with http/https."""
        if isinstance(website_url, str) and website_url.strip():
            # Simple check, could be more robust (e.g., using urllib.parse)
            if re.match(r'^https?://', website_url.strip(), re.IGNORECASE):
                 logging.info(f"Website URL found: {website_url}")
                 return True
        logging.info("No valid website URL found.")
        return False

    def post(self, shared, prep_res, exec_res):
        """Returns action based on whether a valid URL was found."""
        return "has_website" if exec_res else "no_website"

class ScrapeWebsite(Node):
    """Calls the utility to scrape website content."""
    def prep(self, shared):
        return shared.get("company_website") # Should exist if we reached here

    def exec(self, url):
        logging.info(f"Initiating website scrape for: {url}")
        return web_scraper.call_firecrawl(url)

    def post(self, shared, prep_res, exec_res):
        """Stores the scraped content (or error)."""
        shared["website_raw_content"] = exec_res
        if isinstance(exec_res, str) and exec_res.startswith("Error"): # Basic error check
            logging.warning(f"Website scraping resulted in error message: {exec_res}")
        else:
             logging.info(f"Stored website raw content (length: {len(exec_res) if exec_res else 0}).")
        return "default" # Proceed to AnalyzeWebsite

class AnalyzeWebsite(Node):
    """Calls the utility to analyze scraped website content."""
    def prep(self, shared):
        return shared.get("website_raw_content")

    def exec(self, raw_content):
        if not raw_content or (isinstance(raw_content, str) and raw_content.startswith("Error")):
            logging.warning("Skipping website analysis due to missing or error content.")
            return {"error": "No valid website content to analyze"}
        logging.info("Initiating website content analysis.")
        return ai_analyzer.analyze_website_content(raw_content)

    def post(self, shared, prep_res, exec_res):
        """Stores the analysis report (or error dict)."""
        shared["website_report"] = exec_res
        if exec_res.get("error"):
             logging.warning(f"Website analysis failed: {exec_res['error']}")
        else:
            logging.info("Stored website analysis report.")
        return "default" # Proceed to CheckLinkedInExists

class CheckLinkedInExists(Node):
    """Checks if a potentially valid LinkedIn URL is provided."""
    def prep(self, shared):
        return shared.get("linkedin_url")

    def exec(self, linkedin_url):
        """Basic check if URL is non-empty string and contains 'linkedin.com'"""
        if isinstance(linkedin_url, str) and linkedin_url.strip():
            # Simple check, could be more robust
            if "linkedin.com" in linkedin_url.lower():
                 logging.info(f"LinkedIn URL found: {linkedin_url}")
                 return True
        logging.info("No valid LinkedIn URL found.")
        return False

    def post(self, shared, prep_res, exec_res):
        """Returns action based on whether a valid URL was found."""
        return "has_linkedin" if exec_res else "no_linkedin"

class ScrapeLinkedIn(Node):
    """Calls the utility to scrape LinkedIn profile data."""
    def prep(self, shared):
        return shared.get("linkedin_url") # Should exist if we reached here

    def exec(self, url):
        logging.info(f"Initiating LinkedIn profile scrape for: {url}")
        return linkedin_scraper.call_apify_linkedin_profile(url)

    def post(self, shared, prep_res, exec_res):
        """Stores the scraped profile data (or error dict)."""
        shared["linkedin_raw_profile"] = exec_res
        if isinstance(exec_res, dict) and exec_res.get("error"):
            logging.warning(f"LinkedIn scraping failed: {exec_res['error']}")
        else:
            logging.info("Stored LinkedIn raw profile data.")
        return "default" # Proceed to AnalyzeLinkedIn

class AnalyzeLinkedIn(Node):
    """Calls the utility to analyze scraped LinkedIn profile data."""
    def prep(self, shared):
        return shared.get("linkedin_raw_profile")

    def exec(self, raw_profile):
        if not raw_profile or (isinstance(raw_profile, dict) and raw_profile.get("error")):
            logging.warning("Skipping LinkedIn analysis due to missing or error data.")
            return {"error": "No valid LinkedIn profile data to analyze"}
        logging.info("Initiating LinkedIn profile analysis.")
        return ai_analyzer.analyze_linkedin_profile(raw_profile)

    def post(self, shared, prep_res, exec_res):
        """Stores the analysis report (or error dict)."""
        shared["linkedin_report"] = exec_res
        if exec_res.get("error"):
            logging.warning(f"LinkedIn analysis failed: {exec_res['error']}")
        else:
            logging.info("Stored LinkedIn analysis report.")
        return "default" # Proceed to GenerateEmail

class GenerateEmail(Node):
    """Calls the utility to generate a personalized email draft."""
    def prep(self, shared):
        """Packages available context for the generation prompt."""
        context = {
            'lead_name': shared.get('lead_name'),
            'company_name': shared.get('company_name'),
            'website_report': shared.get('website_report'),
            'linkedin_report': shared.get('linkedin_report'),
            'precision_intelligence_report': shared.get('precision_intelligence_report')
        }
        logging.info("Preparing context for email generation, including precision intelligence.")
        return context

    def exec(self, context):
        logging.info("Initiating email generation.")
        return ai_generator.generate_email_draft(context)

    def post(self, shared, prep_res, exec_res):
        """Stores the generated subject and body."""
        # exec_res should be a dict {"subject": "...", "body": "..."} even on error (fallback)
        shared["email_subject"] = exec_res.get("subject", "Error: Subject generation failed")
        shared["email_body"] = exec_res.get("body", "Error: Body generation failed")
        logging.info(f"Stored generated email draft (Subject: {shared['email_subject']}).")
        return "default" # Proceed to StoreResults

class StoreResults(Node):
    """Calls the utility to save the final results to the database."""
    def prep(self, shared):
        """Gathers all relevant data from shared store for saving."""
        # Select specific fields to save, avoiding raw intermediate data unless needed
        data_to_save = {
            "lead_name": shared.get('lead_name'),
            "last_name": shared.get('last_name'),
            "company_name": shared.get('company_name'),
            "company_website": shared.get('company_website'),
            "linkedin_url": shared.get('linkedin_url'),
            # Store reports only if they don't represent an error
            "website_analysis_report": shared.get('website_report') if isinstance(shared.get('website_report'), dict) and not shared.get('website_report').get('error') else None,
            "linkedin_analysis_report": shared.get('linkedin_report') if isinstance(shared.get('linkedin_report'), dict) and not shared.get('linkedin_report').get('error') else None,
            "generated_email_subject": shared.get('email_subject'),
            "generated_email_body": shared.get('email_body')
            # Add timestamps, status flags, etc. as needed
        }
        logging.info("Preparing final data structure for saving.")
        # Remove keys with None values before saving, if desired for DB cleanliness
        # data_to_save = {k: v for k, v in data_to_save.items() if v is not None}
        return data_to_save

    def exec(self, data_to_save):
        logging.info("Initiating save to database.")
        return database.save_to_supabase(data_to_save)

    def post(self, shared, prep_res, exec_res):
        """Logs the success/failure of the save operation."""
        if exec_res:
            logging.info("Successfully saved results to database (simulated).")
        else:
            logging.error("Failed to save results to database (simulated).")
        return "default" # End of flow


# --- Nodes for Precision Lead Intelligence (Tavily Search) ---

class SearchThirdPartySources(Node):
    """Performs targeted Tavily searches for third-party insights."""
    def prep(self, shared):
        """Constructs search queries based on lead/company info."""
        company_name = shared.get('company_name')
        lead_name = shared.get('lead_name')
        # Combine first/last name if available for better search results
        full_name = f"{lead_name} {shared.get('last_name', '')}".strip()
        
        queries = []
        if company_name:
             # Industry/Market Research Queries
             queries.append(f'\"{company_name}\" mentioned in report OR analysis')
             queries.append(f'\"{company_name}\" funding OR acquisition OR partnership news')
             # Sentiment/Review Queries
             queries.append(f'\"{company_name}\" review site:g2.com')
             queries.append(f'\"{company_name}\" review site:capterra.com')
             queries.append(f'\"{company_name}\" reddit OR "forum discussion"')
             # Add more industry-specific review sites if applicable
        
        if full_name and full_name != lead_name: # Check if full name is more than just first name
            # Prospect External Presence Queries
            queries.append(f'\"{full_name}\" speaker OR conference OR webinar')
            queries.append(f'\"{full_name}\" podcast guest OR interview')
            queries.append(f'\"{full_name}\" author industry publication')
        elif lead_name: # Fallback to just first name if that's all we have
             queries.append(f'\"{lead_name}\" {company_name} speaker OR conference') # Combine with company

        if not queries:
             logging.warning("No company or lead name provided, cannot generate third-party search queries.")
        
        logging.info(f"Generated {len(queries)} third-party search queries.")
        return queries # Pass list of queries to exec

    def exec(self, queries):
        """Executes the Tavily search for each query."""
        if not queries:
            return [] # Return empty if no queries were generated
        
        # Import here to avoid circular dependency issues if search moves
        from utils.search import call_tavily_search 
        
        all_results = []
        # Limit the number of queries to avoid excessive API calls/cost
        max_queries_to_run = 6 
        for query in queries[:max_queries_to_run]:
            # Get max 2 results per query to keep context manageable for LLM
            results = call_tavily_search(query, max_results=2)
            if results: # Only add if results are found
                 all_results.extend(results)
            # Optional: Add a small delay between API calls if needed
            # import time
            # time.sleep(0.5)
            
        # Deduplicate results based on URL
        unique_results = []
        seen_urls = set()
        for result in all_results:
            url = result.get('url')
            if url and url not in seen_urls:
                unique_results.append(result)
                seen_urls.add(url)
        
        logging.info(f"Collected {len(unique_results)} unique third-party search results after deduplication.")
        return unique_results

    def post(self, shared, prep_res, exec_res):
        """Stores the aggregated search results."""
        shared['third_party_search_results'] = exec_res
        return "default" # Proceed to AnalyzeThirdPartySources

class AnalyzeThirdPartySources(Node):
    """Analyzes third-party search results using a specific LLM prompt."""
    def prep(self, shared):
        """Formats search results for the LLM prompt."""
        search_results = shared.get('third_party_search_results', [])
        if not search_results:
            logging.warning("No third-party search results found to analyze.")
            return None # Indicate nothing to process

        # Format results into a readable string for the prompt
        formatted_results = "\n\n".join([
            f"Source: {res.get('url', 'N/A')}\nTitle: {res.get('title', 'N/A')}\nContent Snippet: {res.get('content', 'N/A')[:300]}..." 
            for res in search_results
        ])
        
        logging.info(f"Formatted {len(search_results)} search results for analysis prompt.")
        return formatted_results

    def exec(self, formatted_results):
        """Calls the LLM with the Precision Lead Intelligence Agent prompt."""
        if not formatted_results:
            return {"error": "No search results provided for analysis"}
        
        # Import the LLM call function here
        # Note: Assumes call_llm_with_json_output is defined in ai_analyzer
        from utils.ai_analyzer import call_llm_with_json_output, LLM_MODEL
        import datetime

        # Get current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # The detailed prompt provided by the user
        precision_prompt = f"""
You are a precision lead intelligence agent who finds specific, actionable insights from third-party sources only (no LinkedIn or company website data).
You will be evaluated on discovering unique information that automated scraping misses.

current date - {current_date}

## RESEARCHED DATA (from Tavily Search)
{formatted_results}

## RESEARCH PROCESS REMINDER
1. Analyze the RESEARCHED DATA above for Industry & Market Research.
2. Analyze the RESEARCHED DATA above for Public Sentiment & Review Analysis.
3. Analyze the RESEARCHED DATA above for the Prospect's External Presence (if name was searched).

## OUTPUT FORMAT (Respond ONLY with a valid JSON object)
Your findings should be unique and impossible to get from LinkedIn or the company website. Base your analysis **strictly** on the RESEARCHED DATA provided above.

{{
  "industry_context": [
    {{ "point": "string (Market positioning or competitive analysis insight)", "source": "string (URL from RESEARCHED DATA)" }},
    {{ "point": "string (Regulatory or industry trend impact insight)", "source": "string (URL from RESEARCHED DATA)" }}
  ],
  "customer_sentiment": [
    {{ "point": "string (Specific praise or criticism quote)", "source": "string (URL from RESEARCHED DATA)" }},
    {{ "point": "string (Another specific praise/criticism quote)", "source": "string (URL from RESEARCHED DATA)" }}
  ],
  "unique_conversation_angle": {{ "point": "string (One specific, surprising insight based ONLY on the RESEARCHED DATA)", "source": "string (URL from RESEARCHED DATA)" }}
}}

**Quality over quantity - one unique insight is better than five generic points. Cite sources accurately from the RESEARCHED DATA.**
IMPORTANT: Do NOT include information from LinkedIn or the company's own website.
"""
        
        logging.info(f"Calling LLM ({LLM_MODEL}) for Precision Lead Intelligence Analysis.")
        # Use the JSON output helper function
        analysis_result = call_llm_with_json_output(precision_prompt, purpose="Precision Lead Intelligence")
        return analysis_result

    def post(self, shared, prep_res, exec_res):
        """Stores the structured precision intelligence report."""
        shared['precision_intelligence_report'] = exec_res
        if exec_res.get("error"):
             logging.warning(f"Precision Lead Intelligence analysis failed: {exec_res['error']}")
        else:
            logging.info("Stored Precision Lead Intelligence report.")
        return "default" # Proceed to GenerateEmail 