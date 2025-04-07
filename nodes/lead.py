"""Lead-related node classes."""

import logging
from pocketflow import Node
from utils import database

class LoadLeadData(Node):
    """Initial node to load lead data from input parameters."""
    def prep(self, shared):
        """Nothing to prepare, just access the initial input data."""
        return None
        
    def exec(self, prep_res):
        """No computation needed, just pass through."""
        return None
    
    def post(self, shared, prep_res, exec_res):
        """Validate required fields exist in shared data."""
        required_fields = ['lead_name', 'company_name']
        
        # Log what we found
        for field in required_fields:
            if field not in shared or not shared[field]:
                logging.warning(f"Required field '{field}' missing or empty in lead data.")
                return "error"  # Potentially handle error path
        
        logging.info(f"Loaded lead data: {shared['lead_name']} from {shared['company_name']}")
        return "default"  # Proceed to next node (CheckWebsiteExists)


class StoreResults(Node):
    """Calls the utility to save the final results to the database."""
    def prep(self, shared):
        """Gathers all relevant data from shared store for saving."""
        # Select specific fields to save, ensuring keys match DB columns
        data_to_save = {
            "lead_name": shared.get('lead_name'),
            "last_name": shared.get('last_name'),
            "company_name": shared.get('company_name'),
            "company_website": shared.get('company_website'),
            "linkedin_url": shared.get('linkedin_url'),
            # Store reports only if they are valid dicts and don't represent an error
            "website_analysis_report": shared.get('website_report'),
            "linkedin_analysis_report": shared.get('linkedin_report'),
            "precision_intelligence_report": shared.get('precision_intelligence_report'),
            "generated_email_subject": shared.get('email_subject'),
            "generated_email_body": shared.get('email_body')
            # created_at/updated_at are handled by DB
        }
        logging.info("Preparing final data structure for saving, including precision intelligence report.")
        return data_to_save

    def exec(self, data_to_save):
        logging.info("Initiating save to database.")
        return database.save_to_supabase(data_to_save)

    def post(self, shared, prep_res, exec_res):
        """Logs the success/failure of the save operation."""
        if exec_res:
            logging.info("Successfully saved results to database.")
        else:
            logging.error("Failed to save results to database.")
        return "default" # End of flow 