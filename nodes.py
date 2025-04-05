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
            'website_report': shared.get('website_report'), # Could be None or error dict
            'linkedin_report': shared.get('linkedin_report') # Could be None or error dict
        }
        logging.info("Preparing context for email generation.")
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