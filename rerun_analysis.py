# rerun_analysis.py
import pickle
import argparse
import logging
import os
import json
from pathlib import Path
from typing import Optional

# Import necessary generator functions (adjust paths if needed)
from utils.generators.website_analysis import generate_website_analysis
from utils.generators.linkedin_analysis import generate_linkedin_analysis
from utils.generators.third_party_analysis import generate_analysis_prompt

# We might need the AI call function if generators only return prompts
from utils import ai

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions ---
def load_cache(cache_file_path: Path) -> dict | None:
    """Loads the shared_store from a pickle cache file."""
    if not cache_file_path.is_file():
        logging.error(f"Cache file not found: {cache_file_path}")
        return None
    try:
        with open(cache_file_path, "rb") as f:
            shared_store = pickle.load(f)
        logging.info(f"Successfully loaded cache from: {cache_file_path}")
        return shared_store
    except Exception as e:
        logging.error(f"Failed to load cache file {cache_file_path}: {e}", exc_info=True)
        return None

def rerun_website(shared_store: dict, model: Optional[str] = None):
    """Re-runs website analysis using raw data from shared_store."""
    logging.info(f"--- Re-running Website Analysis (Model: {model or 'Default'}) ---")
    raw_content = shared_store.get('raw_website_content')
    company_name = shared_store.get('company_name', '')
    website_url = shared_store.get('company_website', '') # Original URL for context

    if not raw_content:
        logging.warning("No 'raw_website_content' found in cache. Skipping website re-analysis.")
        return

    # Limit content length (similar to original node) - adjust as needed
    max_content_length = 15000
    if len(raw_content) > max_content_length:
        logging.info(f"Truncating raw website content from {len(raw_content)} to {max_content_length} chars for analysis")
        raw_content = raw_content[:max_content_length]

    try:
        # Pass the model argument to the generator
        new_report = generate_website_analysis(
            company_name=company_name,
            website_url=website_url,
            website_content=raw_content, # Pass the raw content
            model=model # Pass the specified model
        )
        print("\n>>> New Website Analysis Report:")
        print(new_report)
        print("-" * 30)
    except Exception as e:
        logging.error(f"Error during website re-analysis: {e}", exc_info=True)

def rerun_linkedin(shared_store: dict, model: Optional[str] = None):
    """Re-runs LinkedIn analysis using raw data from shared_store."""
    logging.info(f"--- Re-running LinkedIn Analysis (Model: {model or 'Default'}) ---")
    raw_content = shared_store.get('raw_linkedin_content')
    company_name = shared_store.get('company_name', '')
    lead_first_name = shared_store.get('lead_first_name', '')
    lead_last_name = shared_store.get('lead_last_name', '')
    linkedin_url = shared_store.get('linkedin_url', '') # Original URL

    if not raw_content:
        logging.warning("No 'raw_linkedin_content' found in cache. Skipping LinkedIn re-analysis.")
        return

    # Limit content length
    max_content_length = 15000
    if len(raw_content) > max_content_length:
        logging.info(f"Truncating raw LinkedIn content from {len(raw_content)} to {max_content_length} chars")
        raw_content = raw_content[:max_content_length]

    try:
        # Pass the model argument to the generator
        new_report = generate_linkedin_analysis(
            lead_first_name=lead_first_name,
            lead_last_name=lead_last_name,
            company_name=company_name,
            linkedin_url=linkedin_url,
            linkedin_content=raw_content, # Pass raw content
            model=model # Pass the specified model
        )
        print("\n>>> New LinkedIn Analysis Report:")
        print(new_report)
        print("-" * 30)
    except Exception as e:
        logging.error(f"Error during LinkedIn re-analysis: {e}", exc_info=True)

def rerun_third_party(shared_store: dict, model: Optional[str] = None):
    """Re-runs Third-Party analysis using raw data from shared_store."""
    logging.info(f"--- Re-running Third-Party Analysis (Model: {model or 'Default'}) ---")
    raw_results = shared_store.get('raw_third_party_search_results')
    company_name = shared_store.get('company_name', '')
    lead_first_name = shared_store.get('lead_first_name', '')
    lead_last_name = shared_store.get('lead_last_name', '')
    # Note: The date will be the current date when re-running analysis
    from datetime import date
    current_date_today = date.today()

    if not raw_results:
        logging.warning("No 'raw_third_party_search_results' found in cache. Skipping third-party re-analysis.")
        return

    try:
        # Generate the prompt first
        analysis_prompt = generate_analysis_prompt(
            lead_first_name=lead_first_name,
            lead_last_name=lead_last_name,
            company_name=company_name,
            sources=raw_results, # Pass raw search results
            current_date=current_date_today
        )
        # Pass the model argument to the direct call_llm
        new_report = ai.call_llm(
            prompt=analysis_prompt,
            model=model # Pass the specified model
            # Add other relevant parameters like temperature if needed
        )
        print("\n>>> New Third-Party Analysis Report:")
        print(new_report)
        print("-" * 30)
    except Exception as e:
        logging.error(f"Error during third-party re-analysis: {e}", exc_info=True)


# --- Main Execution ---
def main():
    parser = argparse.ArgumentParser(description="Re-run analysis steps on cached raw data.")
    parser.add_argument(
        "--cache-file",
        required=True,
        type=Path,
        help="Path to the .pkl cache file generated by the web app."
    )
    parser.add_argument(
        "--reanalyze",
        nargs='+', # Allows multiple values
        choices=['website', 'linkedin', 'third-party'],
        required=True,
        help="Which analysis section(s) to re-run."
    )
    parser.add_argument(
        "--model",
        default=None, # Default is None, letting utils.ai handle its default
        help="Specify AI model identifier (e.g., 'gpt-4o-mini', 'groq/meta-llama/llama-4-scout-17b-16e-instruct')"
    )

    args = parser.parse_args()

    shared_store = load_cache(args.cache_file)
    if not shared_store:
        return # Error handled in load_cache

    logging.info(f"Re-analyzing sections: {', '.join(args.reanalyze)}")
    if args.model:
        logging.info(f"Using specified model: {args.model}")

    if 'website' in args.reanalyze:
        rerun_website(shared_store, model=args.model)

    if 'linkedin' in args.reanalyze:
        rerun_linkedin(shared_store, model=args.model)

    if 'third-party' in args.reanalyze:
        rerun_third_party(shared_store, model=args.model)

    logging.info("Re-analysis script finished.")


if __name__ == "__main__":
    main() 