"""Website-related node classes."""

import logging
from pocketflow import Node
from utils import scraper, search
from utils.generators import generate_website_analysis

class CheckWebsiteExists(Node):
    """Checks if a company website can be found."""
    def prep(self, shared):
        """Prepare search query for company website."""
        # Combine company name with typical search terms
        company_name = shared['company_name']
        search_query = f"{company_name} official website"
        logging.info(f"Searching for website of {company_name}")
        return search_query

    def exec(self, search_query):
        """Search for the company website."""
        # Use web search utility (returns list of results)
        search_results = search.call_tavily_search(search_query, max_results=5)
        return search_results

    def post(self, shared, prep_res, exec_res):
        """Extract website URL from search results and store in shared."""
        if not exec_res:
            logging.warning(f"No search results found for {shared['company_name']} website")
            return "no_website"

        # Take first result's URL that matches typical website patterns
        # Could be improved with more sophisticated filtering logic
        website_url = None
        
        # Extract domain from first result that's not a social media site
        for result in exec_res:
            url = result.get('url', '')
            # Skip common non-company websites
            if any(domain in url for domain in [
                'linkedin.com', 'facebook.com', 'twitter.com', 
                'instagram.com', 'youtube.com', 'crunchbase.com'
            ]):
                continue
                
            website_url = url
            break

        if website_url:
            logging.info(f"Found potential company website: {website_url}")
            shared['company_website'] = website_url
            return "default"  # Proceed to scraping
        else:
            logging.warning(f"Could not identify a valid company website for {shared['company_name']}")
            return "no_website"  # Skip website analysis


class ScrapeWebsite(Node):
    """Scrapes content from the company website."""
    def prep(self, shared):
        """Get the company website URL."""
        website_url = shared.get('company_website')
        if not website_url:
            logging.warning("No website URL found in shared data")
            return None
        logging.info(f"Preparing to scrape: {website_url}")
        return website_url

    def exec(self, website_url):
        """Scrape the website content."""
        if not website_url:
            return None
            
        try:
            scraped_content = scraper.scrape_website(website_url)
            return scraped_content
        except Exception as e:
            logging.error(f"Error scraping {website_url}: {str(e)}")
            return None

    def post(self, shared, prep_res, exec_res):
        """Store scraped content in shared or handle failure."""
        if exec_res:
            # Successfully scraped content
            shared['website_content'] = exec_res
            logging.info(f"Successfully scraped website content: {len(exec_res)} characters")
            return "default"  # Proceed to analysis
        else:
            # Failed to scrape
            logging.warning("Website scraping failed or returned no content")
            return "scrape_failed"  # Skip website analysis


class AnalyzeWebsite(Node):
    """Analyzes the scraped website content."""
    def prep(self, shared):
        """Get the website content and company name."""
        website_content = shared.get('website_content', '')
        company_name = shared.get('company_name', '')
        website_url = shared.get('company_website', '')
        
        # If no content, nothing to analyze
        if not website_content:
            logging.warning("No website content available for analysis")
            return None
            
        logging.info(f"Preparing website content ({len(website_content)} chars) for analysis")
        return {
            'content': website_content,
            'company_name': company_name,
            'website_url': website_url
        }
        
    def exec(self, prep_res):
        """Generate analysis of website content using LLM."""
        if not prep_res:
            return "No website content to analyze."
            
        website_content = prep_res['content']
        company_name = prep_res['company_name']
        website_url = prep_res['website_url']
        
        # Limit content length if too large for LLM
        max_content_length = 15000  # Adjust based on LLM context limits
        if len(website_content) > max_content_length:
            logging.info(f"Truncating website content from {len(website_content)} to {max_content_length} chars")
            website_content = website_content[:max_content_length]
        
        # Call the specific generator function
        analysis_report = generate_website_analysis(
            company_name=company_name,
            website_url=website_url,
            website_content=website_content
        )
        return analysis_report

    def post(self, shared, prep_res, exec_res):
        """Store the analysis report or error in shared."""
        if not exec_res or exec_res.startswith("Error"):
            logging.warning(f"Website analysis failed: {exec_res}")
            shared['website_report'] = f"Analysis failed: {exec_res}"
        else:
            logging.info("Successfully generated website analysis report")
            shared['website_report'] = exec_res
            
        return "default"  # Continue flow regardless 