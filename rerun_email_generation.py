# rerun_email_generation.py
"""Script to re-run email generation with different models using cached analysis data."""

import pickle
import argparse
import logging
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import the target generator function
from utils.generators.email import generate_email

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a default list of models to test if none are provided via arguments
# You can customize this list
DEFAULT_MODELS_TO_TEST = [
    "gpt-4o-mini",            # Default OpenAI
    "gemini-2.5-pro-preview-03-25",
    # "gemini-1.5-flash-latest", # Default Gemini
    # "llama3-8b-8192",         # Default Groq Llama3 8b
    "meta-llama/llama-4-scout-17b-16e-instruct", # The one used originally in generate_email
    # Add other models you want to test by default
]

# --- Helper Functions ---
def load_cache(cache_file_path: Path) -> Optional[Dict[str, Any]]:
    """Loads the shared_store dictionary from a pickle cache file."""
    if not cache_file_path.is_file():
        logging.error(f"Cache file not found: {cache_file_path}")
        return None
    try:
        with open(cache_file_path, "rb") as f:
            shared_store = pickle.load(f)
        logging.info(f"Successfully loaded cache from: {cache_file_path}")
        if not isinstance(shared_store, dict):
            logging.error(f"Cache file {cache_file_path} did not contain a dictionary.")
            return None
        return shared_store
    except Exception as e:
        logging.error(f"Failed to load cache file {cache_file_path}: {e}", exc_info=True)
        return None

# --- Main Execution ---
def main():
    parser = argparse.ArgumentParser(
        description="Re-run email generation step with different models using cached analysis data."
    )
    parser.add_argument(
        "--cache-file",
        required=True,
        type=Path,
        help="Path to the .pkl cache file containing the shared_store from a previous run."
    )
    parser.add_argument(
        "--models",
        nargs='+',
        default=None,
        help=f"Space-separated list of model identifiers to test. Defaults to: {', '.join(DEFAULT_MODELS_TO_TEST)}"
    )
    parser.add_argument(
        "--product-service",
        required=True,
        type=str,
        help="Description of the product/service you are selling (used in email generation)."
    )

    args = parser.parse_args()

    shared_store = load_cache(args.cache_file)
    if not shared_store:
        return # Error handled in load_cache

    # Determine which models to test
    models_to_test = args.models if args.models else DEFAULT_MODELS_TO_TEST

    # Extract necessary data from the cache
    try:
        lead_first_name = shared_store.get('lead_first_name', '')
        lead_last_name = shared_store.get('lead_last_name', '')
        company_name = shared_store['company_name'] # Assume company name is essential
        company_website = shared_store.get('company_website', '')
        linkedin_url = shared_store.get('linkedin_url', '')
        website_report = shared_store.get('website_report', '') # Report output, not raw
        linkedin_report = shared_store.get('linkedin_report', '') # Report output, not raw
        precision_intelligence_report = shared_store.get('precision_intelligence_report', '') # Report output
    except KeyError as e:
        logging.error(f"Essential key missing from cache file {args.cache_file}: {e}. Cannot proceed.")
        return

    lead_full_name = f"{lead_first_name} {lead_last_name}".strip()
    target_info = f"Lead: {lead_full_name or '[No Name]'}, Company: {company_name}"
    logging.info(f"Target data loaded for: {target_info}")
    logging.info(f"Product/Service: {args.product_service}")
    logging.info(f"Models to test: {', '.join(models_to_test)}")

    # Loop through the selected models and generate emails
    for model_id in models_to_test:
        print(f"\n--- Testing Email Generation with Model: {model_id} ---")
        logging.info(f"Calling generate_email for {target_info} using model: {model_id}")

        try:
            email_result = generate_email(
                lead_first_name=lead_first_name,
                lead_last_name=lead_last_name,
                company_name=company_name,
                product_service=args.product_service, # From command line args
                company_website=company_website,
                linkedin_url=linkedin_url,
                website_report=website_report,
                linkedin_report=linkedin_report,
                precision_intelligence_report=precision_intelligence_report,
                model=model_id, # Pass the current model from the loop
                dev_local_mode=True # IMPORTANT: Enable caching per model
            )

            if isinstance(email_result, dict) and 'subject' in email_result and 'body' in email_result:
                print(f"Subject: {email_result['subject']}")
                print(f"Body:\n{email_result['body']}")
            else:
                logging.warning(f"Received unexpected result structure for model {model_id}: {email_result}")
                print(f"Result (unexpected format): {email_result}")

        except Exception as e:
            logging.error(f"Error during email generation for model {model_id}: {e}", exc_info=True)
            print(f"ERROR occurred for model {model_id}. Check logs.")

        print("-" * 30)

    logging.info(f"Finished re-running email generation for: {target_info}")

if __name__ == "__main__":
    main() 