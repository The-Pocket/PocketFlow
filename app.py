"""Flask web application for the Personalized Email Generation tool."""

import logging
import json
import os
import argparse
import pickle
from pathlib import Path
from flask import Flask, render_template, request, flash

# Import the flow creation function and potentially nodes/utils if needed directly
from flow import create_v1_lead_processing_flow
# Assuming pocketflow is installed and accessible
from pocketflow import Flow 

# Configure logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create cache directory if it doesn't exist
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run the Personalized Email Generation app")
parser.add_argument('--dev-local', action='store_true', help='Run in development mode using cached API responses')
args = parser.parse_args()

# Set development mode flag globally
DEV_LOCAL_MODE = args.dev_local
if DEV_LOCAL_MODE:
    logging.info("Running in DEV-LOCAL mode. Using cached API responses when available.")

app = Flask(__name__)
# Secret key needed for flashing messages
app.secret_key = 'your_very_secret_key_here' # Change this in production!

# --- Backend Processing Logic ---

def process_lead_with_flow(lead_info: dict) -> dict:
    """
    Runs the V1 PocketFlow for a single lead and returns the results.
    (Similar to run_single_lead from main.py, adapted for web app context)
    """
    lead_full_name = f"{lead_info.get('lead_first_name', '')} {lead_info.get('lead_last_name', '')}".strip() or "N/A"
    logging.info(f"--- Starting web request processing for lead: {lead_full_name} ---")
    
    # Create a unique cache key based on the lead information
    cache_key = f"{lead_info.get('lead_first_name', '')}-{lead_info.get('company_name', '')}-{lead_info.get('company_website', '')}-{lead_info.get('linkedin_url', '')}"
    cache_key = cache_key.replace(" ", "_").replace("/", "_").replace(":", "_").lower()
    cache_file = CACHE_DIR / f"{cache_key}.pkl"
    
    # Check if we have cached results and we're in dev-local mode
    if DEV_LOCAL_MODE and cache_file.exists():
        try:
            logging.info(f"Loading cached results for {cache_key}")
            with open(cache_file, "rb") as f:
                shared_store = pickle.load(f)
            return shared_store
        except Exception as e:
            logging.warning(f"Failed to load cache for {cache_key}: {e}")
    
    # Create a fresh shared store, pre-populated with lead info
    shared_store = lead_info.copy() 
    
    # Store the dev mode flag in the shared store so nodes can access it
    shared_store["dev_local_mode"] = DEV_LOCAL_MODE
    
    try:
        # Create the flow instance
        # Consider caching the flow creation if it's expensive, but for now, create each time
        v1_flow: Flow = create_v1_lead_processing_flow()
        
        # Run the flow
        v1_flow.run(shared=shared_store)
        
        logging.info(f"--- Finished web request processing for lead: {lead_full_name} ---")
        
        # Cache the results if in dev-local mode
        if DEV_LOCAL_MODE:
            try:
                logging.info(f"Caching results for {cache_key}")
                with open(cache_file, "wb") as f:
                    pickle.dump(shared_store, f)
            except Exception as e:
                logging.warning(f"Failed to cache results for {cache_key}: {e}")
        
        # Extract key results for display 
        # Return the whole shared store for now, template can pick needed fields
        return shared_store

    except Exception as e:
        lead_full_name_for_error = f"{lead_info.get('lead_first_name', '')} {lead_info.get('lead_last_name', '')}".strip() or "N/A"
        logging.error(f"Error during PocketFlow execution for lead {lead_full_name_for_error}: {e}", exc_info=True)
        # Return an error structure that the template can recognize
        return {"error": f"An internal error occurred during processing: {e}"}

# --- Flask Routes ---

@app.route('/', methods=['GET'])
def index():
    """Displays the input form."""
    return render_template('index.html', results=None, lead_input=None)

@app.route('/process', methods=['POST'])
def process():
    """Processes the form submission, runs the flow, and displays results."""
    # Get data from form
    lead_input = {
        "lead_first_name": request.form.get('lead_first_name', '').strip(),
        "lead_last_name": request.form.get('lead_last_name', '').strip(),
        "company_name": request.form.get('company_name', '').strip(),
        "company_website": request.form.get('company_website', '').strip(),
        "linkedin_url": request.form.get('linkedin_url', '').strip(),
        "product_service": request.form.get('product_service', '').strip()
    }
    
    # Basic validation (can be more sophisticated)
    if not lead_input['lead_first_name'] and not lead_input['company_name']:
        flash("Please provide at least a Lead Name or Company Name.", "warning")
        return render_template('index.html', results=None, lead_input=lead_input)
    if not lead_input['company_website'] and not lead_input['linkedin_url']:
         flash("Please provide at least a Company Website or LinkedIn URL for analysis.", "warning")
         return render_template('index.html', results=None, lead_input=lead_input)

    logging.info(f"Received lead data from form: {lead_input}")
    
    # Run the backend processing
    results = process_lead_with_flow(lead_input)
    
    if results.get("error"):
         flash(f"Processing Error: {results['error']}", "danger")
         # Render index but pass back original input and potentially partial results if available
         return render_template('index.html', results=None, lead_input=lead_input) 
    else:
         flash("Lead processed successfully!", "success")
         # Pass results and original input back to the template
         return render_template('index.html', results=results, lead_input=lead_input)

if __name__ == '__main__':
    # Run the Flask app
    # Debug=True is helpful for development but should be False in production
    logging.info("Starting Flask development server...")
    app.run(debug=True, port=5001) # Use port 5001 to avoid conflicts if needed 