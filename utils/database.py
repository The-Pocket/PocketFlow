"""Utility functions for database interactions, e.g., using Supabase."""

import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE") # Use service role key for server-side operations
supabase: Client | None = None
if url and key:
    try:
        supabase = create_client(url, key)
        logging.info("Supabase client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    logging.warning("Supabase URL or Key not found in environment variables. Database utility will not function.")

def save_to_supabase(lead_data: dict) -> bool:
    """
    Saves lead data to the 'leads' table in Supabase using upsert.
    Relies on the UNIQUE constraint on 'linkedin_url' for conflict resolution if URL is present.

    Args:
        lead_data: A dictionary containing the lead record (keys should match table columns).

    Returns:
        True if successful, False otherwise.
    """
    if not supabase:
        logging.error("Supabase client not initialized. Cannot save data.")
        return False

    table_name = "leads"
    # Prepare data: remove keys with None values? Supabase handles None, so maybe keep for consistency?
    # data_to_upsert = {k: v for k, v in lead_data.items() if v is not None}
    data_to_upsert = lead_data # Keep None values
    
    lead_full_name = f"{data_to_upsert.get('lead_first_name', '')} {data_to_upsert.get('lead_last_name', '')}".strip() or "Unknown Lead"
    logging.info(f"Attempting to upsert data to Supabase table '{table_name}'. Lead: {lead_full_name}")
    # print("Data for upsert:", data_to_upsert)

    try:
        # If linkedin_url is provided and intended as the conflict target for upsert:
        # response = supabase.table(table_name).upsert(data_to_upsert, on_conflict='linkedin_url').execute()
        
        # Simpler approach: Insert. Let UNIQUE constraint handle conflicts if linkedin_url exists.
        # Or use upsert without on_conflict if relying on primary key (which we generate on insert)
        # Using insert for now, assuming we mostly add new leads via this flow.
        # If you need to UPDATE based on linkedin_url, use upsert with on_conflict.
        response = supabase.table(table_name).insert(data_to_upsert).execute()
        
        logging.info(f"Supabase insert response status: {response.data}") # Check response structure
        # Check if response indicates success, structure might vary
        if response.data:
            logging.info(f"Successfully saved/updated lead '{lead_full_name}' in Supabase.")
            return True
        else:
            # Supabase errors might be in response.error instead
            error_info = getattr(response, 'error', 'Unknown error')
            logging.error(f"Supabase insert failed for lead '{lead_full_name}'. Error: {error_info}")
            return False

    except Exception as e:
        logging.error(f"Error interacting with Supabase table '{table_name}': {e}")
        return False

if __name__ == '__main__':
    # Example usage for testing - Requires .env file with Supabase credentials
    print("\n--- Testing Supabase Save --- (Requires .env and table creation)")
    
    if not supabase:
        print("Skipping test: Supabase client not initialized.")
    else:
        test_lead_for_db = {
            # "id": "some-uuid", # Don't include id if inserting new
            "lead_first_name": "DB Test User",
            "lead_last_name": "Supabase",
            "company_name": "Test Corp DB",
            "company_website": "https://db-test.example",
            # Use a unique linkedin_url for testing insertion/conflict
            "linkedin_url": f"https://linkedin.com/in/db-test-user-{os.urandom(3).hex()}", 
            "website_analysis_report": {
                "analysis_type": "website",
                "products_services": ["DB Test Product"],
                "target_audience": "Testers",
                "value_proposition": "Testable DB Interaction",
                "raw_length": 500
            },
            "linkedin_analysis_report": {
                "analysis_type": "linkedin_profile",
                "career_summary": "Test user profile.",
                "key_skills": ["Testing", "Supabase"],
                "recent_focus": "Database Integration",
                "name": "DB Test User Supabase"
            },
            "generated_email_subject": "Testing Supabase Insert",
            "generated_email_body": "This is a test entry from database.py."
            # created_at and updated_at will be handled by DB defaults/triggers
        }

        success = save_to_supabase(test_lead_for_db)
        print(f"\nSave successful: {success}")
        if success:
            lead_full_name_test = f"{test_lead_for_db['lead_first_name']} {test_lead_for_db['lead_last_name']}".strip()
            print(f"Check your Supabase 'leads' table for lead: {lead_full_name_test} with LinkedIn URL: {test_lead_for_db['linkedin_url']}")
        print("---------------------------") 