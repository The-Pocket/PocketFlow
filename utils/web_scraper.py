"""Utility function for scraping web content, e.g., using Firecrawl."""

import os
import logging
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Firecrawl client
firecrawl_api_key = os.environ.get("FIRECRAWL_API_KEY")
app: FirecrawlApp | None = None
if firecrawl_api_key:
    try:
        app = FirecrawlApp(api_key=firecrawl_api_key)
        logging.info("Firecrawl client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Firecrawl client: {e}")
        app = None
else:
    logging.warning("FIRECRAWL_API_KEY not found in environment variables. Web scraping utility will not function.")

def call_firecrawl(url: str) -> str | None:
    """
    Scrapes website content using the Firecrawl API.

    Args:
        url: The URL of the website to scrape.

    Returns:
        A string containing the scraped markdown content, or None if an error occurs.
    """
    if not app:
        logging.error("Firecrawl client not initialized. Cannot scrape website.")
        return None # Indicate failure clearly

    logging.info(f"Attempting to scrape website: {url} with Firecrawl...")
    try:
        # Use crawl=False for single page scrape, returns markdown by default
        # You can adjust params for different needs, e.g., pageOptions for screenshots
        scraped_data = app.scrape_url(url, params={'onlyMainContent': True})
        
        # Check if scraping was successful and content exists
        if scraped_data and 'markdown' in scraped_data:
             content = scraped_data['markdown']
             logging.info(f"Successfully scraped content from {url} (Length: {len(content)}).")
             return content
        elif scraped_data and 'content' in scraped_data: # Fallback to raw content if markdown isn't there
             content = scraped_data['content']
             logging.info(f"Successfully scraped raw content from {url} (Length: {len(content)}). Markdown format preferred but not found.")
             return content
        else:
            logging.warning(f"Firecrawl returned no content for {url}. Response: {scraped_data}")
            return None
            
    except Exception as e:
        logging.error(f"Error scraping {url} with Firecrawl: {e}", exc_info=True)
        return None # Indicate failure clearly

if __name__ == '__main__':
    # Example usage for testing - Requires .env file with FIRECRAWL_API_KEY
    print("\n--- Testing Firecrawl Scraper --- (Requires .env)")
    
    if not app:
        print("Skipping test: Firecrawl client not initialized.")
    else:
        test_url = "https://www.google.com" # Use Google for testing
        content = call_firecrawl(test_url)
        
        if content:
            print(f"\n--- Scraped Content (Markdown/Raw) for {test_url} ---")
            # Print first 500 characters for brevity
            print(content[:500] + "...") 
            print("----------------------------------------------")
        else:
            print(f"\nFailed to scrape content from {test_url}.")
        print("-------------------------------------------") 