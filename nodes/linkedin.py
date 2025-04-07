"""LinkedIn-related node classes."""

import logging
from pocketflow import Node
from utils import scraper, search
from utils.generators import generate_linkedin_analysis

class CheckLinkedInExists(Node):
    """Checks if a LinkedIn profile exists for the lead/company."""
    def prep(self, shared):
        """Prepare search query for LinkedIn profile."""
        company_name = shared.get('company_name', '')
        lead_first_name = shared.get('lead_first_name', '')
        lead_last_name = shared.get('lead_last_name', '')
        
        # Create search query based on available info
        lead_full_name_for_search = f"{lead_first_name} {lead_last_name}".strip()
        if lead_full_name_for_search and company_name:
            search_query = f"{lead_full_name_for_search} {company_name} linkedin"
        elif company_name:
            search_query = f"{company_name} linkedin"
        else:
            logging.warning("Insufficient data to search for LinkedIn profile")
            return None
            
        logging.info(f"Searching for LinkedIn profile with query: {search_query}")
        return search_query
        
    def exec(self, search_query):
        """Execute search for LinkedIn profile."""
        if not search_query:
            return None
            
        # Search web for LinkedIn profile
        search_results = search.web_search(search_query, max_results=5)
        return search_results
        
    def post(self, shared, prep_res, exec_res):
        """Extract LinkedIn URL from search results."""
        if not exec_res:
            logging.warning("No search results found for LinkedIn profile")
            return "no_linkedin"
            
        # Look for LinkedIn URLs in results
        linkedin_url = None
        for result in exec_res:
            url = result.get('url', '')
            if 'linkedin.com/in/' in url or 'linkedin.com/company/' in url:
                linkedin_url = url
                break
                
        if linkedin_url:
            logging.info(f"Found LinkedIn profile: {linkedin_url}")
            shared['linkedin_url'] = linkedin_url
            return "default"  # Continue to LinkedIn scraping
        else:
            logging.warning("No LinkedIn profile URL found in search results")
            return "no_linkedin"  # Skip LinkedIn analysis


class ScrapeLinkedIn(Node):
    """Scrapes content from the LinkedIn profile."""
    def prep(self, shared):
        """Get the LinkedIn URL."""
        linkedin_url = shared.get('linkedin_url')
        if not linkedin_url:
            logging.warning("No LinkedIn URL found in shared data")
            return None
        logging.info(f"Preparing to scrape LinkedIn: {linkedin_url}")
        return linkedin_url
        
    def exec(self, linkedin_url):
        """Scrape the LinkedIn profile content."""
        if not linkedin_url:
            return None
            
        try:
            # Use scraper utility to get LinkedIn content
            scraped_content = scraper.scrape_linkedin(linkedin_url)
            return scraped_content
        except Exception as e:
            logging.error(f"Error scraping LinkedIn {linkedin_url}: {str(e)}")
            return None
            
    def post(self, shared, prep_res, exec_res):
        """Store scraped LinkedIn content in shared."""
        if exec_res:
            shared['linkedin_content'] = exec_res
            logging.info(f"Successfully scraped LinkedIn content: {len(exec_res)} characters")
            return "default"  # Proceed to analysis
        else:
            logging.warning("LinkedIn scraping failed or returned no content")
            return "scrape_failed"  # Skip LinkedIn analysis


class AnalyzeLinkedIn(Node):
    """Analyzes the scraped LinkedIn content."""
    def prep(self, shared):
        """Get the LinkedIn content and related info."""
        linkedin_content = shared.get('linkedin_content', '')
        company_name = shared.get('company_name', '')
        lead_first_name = shared.get('lead_first_name', '')
        lead_last_name = shared.get('lead_last_name', '')
        linkedin_url = shared.get('linkedin_url', '')
        
        # If no content, nothing to analyze
        if not linkedin_content:
            logging.warning("No LinkedIn content available for analysis")
            return None
            
        logging.info(f"Preparing LinkedIn content ({len(linkedin_content)} chars) for analysis")
        return {
            'content': linkedin_content,
            'company_name': company_name,
            'lead_first_name': lead_first_name,
            'lead_last_name': lead_last_name,
            'linkedin_url': linkedin_url
        }
        
    def exec(self, prep_res):
        """Generate analysis of LinkedIn content using LLM."""
        if not prep_res:
            return "No LinkedIn content to analyze."
            
        linkedin_content = prep_res['content']
        company_name = prep_res['company_name']
        lead_first_name = prep_res['lead_first_name']
        lead_last_name = prep_res['lead_last_name']
        linkedin_url = prep_res['linkedin_url']
        
        # Limit content length if too large for LLM
        max_content_length = 15000  # Adjust based on LLM context limits
        if len(linkedin_content) > max_content_length:
            logging.info(f"Truncating LinkedIn content from {len(linkedin_content)} to {max_content_length} chars")
            linkedin_content = linkedin_content[:max_content_length]
            
        # Call the specific generator function
        analysis_report = generate_linkedin_analysis(
            lead_first_name=lead_first_name,
            lead_last_name=lead_last_name,
            company_name=company_name,
            linkedin_url=linkedin_url,
            linkedin_content=linkedin_content
        )
        return analysis_report
    
    def post(self, shared, prep_res, exec_res):
        """Store the LinkedIn analysis report in shared."""
        if not exec_res or exec_res.startswith("Error"):
            logging.warning(f"LinkedIn analysis failed: {exec_res}")
            shared['linkedin_report'] = f"Analysis failed: {exec_res}"
        else:
            logging.info("Successfully generated LinkedIn analysis report")
            shared['linkedin_report'] = exec_res
            
        return "default"  # Continue flow regardless 