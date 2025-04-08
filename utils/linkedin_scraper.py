"""Utility function for scraping LinkedIn profiles, e.g., using Apify."""

import os
import logging
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Apify client
apify_api_key = os.environ.get("APIFY_API_KEY") # Changed from APIFY_API_TOKEN based on user input
apify_client: ApifyClient | None = None
if apify_api_key:
    try:
        apify_client = ApifyClient(apify_api_key)
        logging.info("Apify client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Apify client: {e}")
        apify_client = None
else:
    logging.warning("APIFY_API_KEY not found in environment variables. LinkedIn scraping utility will not function.")

# Actor ID provided by user
LINKEDIN_PROFILE_ACTOR_ID = "dev_fusion/Linkedin-Profile-Scraper"

def call_apify_linkedin_profile(url: str) -> dict:
    """
    Scrapes a LinkedIn profile using the specified Apify Actor.

    Args:
        url: The URL of the LinkedIn profile.

    Returns:
        A dictionary containing scraped profile data, or an error dictionary.
    """
    if not apify_client:
        logging.error("Apify client not initialized. Cannot scrape LinkedIn profile.")
        return {"error": "Apify client not initialized"}

    logging.info(f"Attempting to scrape LinkedIn profile: {url} via Apify Actor: {LINKEDIN_PROFILE_ACTOR_ID}")

    try:
        # Get the Actor client
        actor_client = apify_client.actor(LINKEDIN_PROFILE_ACTOR_ID)
        
        # Prepare the Actor input as specified
        run_input = { "profileUrls": [url] }
        
        # Start the Actor run and wait for it to finish
        # Note: This is a synchronous call and might take some time.
        # For production, consider using .start() and webhooks or polling.
        logging.info(f"Calling Apify Actor with input: {run_input}")
        run = actor_client.call(run_input=run_input, memory_mbytes=2048, timeout_secs=120) # Increased memory/timeout
        logging.info(f"Apify Actor run finished. Run ID: {run.get('id') if run else 'N/A'}, Status: {run.get('status') if run else 'N/A'}")

        # Check run status
        if not run or run.get('status') != 'SUCCEEDED':
             logging.error(f"Apify Actor run for {url} did not succeed. Status: {run.get('status') if run else 'N/A'}. Run details: {run}")
             return {"error": f"Apify Actor run failed or timed out. Status: {run.get('status') if run else 'N/A'}"}

        # Fetch Actor results from the run's default dataset
        dataset_client = apify_client.dataset(run["defaultDatasetId"])
        profile_data_list = list(dataset_client.iterate_items())
        
        if profile_data_list:
             logging.info(f"Successfully retrieved {len(profile_data_list)} item(s) from Apify dataset for {url}.")
             # Assuming the actor returns one item per URL in the input list
             return profile_data_list[0] 
        else:
             logging.warning(f"Apify Actor run succeeded but returned no items in the dataset for {url}.")
             return {"error": "No data found by Apify Actor in the dataset"}
             
    except Exception as e:
        logging.error(f"Error calling Apify Actor {LINKEDIN_PROFILE_ACTOR_ID} for {url}: {e}", exc_info=True)
        return {"error": f"Apify Actor call failed with exception: {e}"}

if __name__ == '__main__':
    # Example usage for testing - Requires .env file with APIFY_API_KEY
    print("\n--- Testing Apify LinkedIn Scraper --- (Requires .env)")

    if not apify_client:
        print("Skipping test: Apify client not initialized.")
    else:
        # Use the profile provided by user for testing
        test_url = "https://www.linkedin.com/in/caylott"
        profile = call_apify_linkedin_profile(test_url)
        
        print(f"\n--- Apify Scrape Result for {test_url} ---")
        import json
        # Print first 1000 chars for brevity
        profile_str = json.dumps(profile, indent=2, default=str)
        print(profile_str[:1000] + ("..." if len(profile_str) > 1000 else ""))
        print("-------------------------------------------") 