"""Flask web application for the Personalized Email Generation tool."""

import logging
import json
from flask import Flask, render_template, request, flash

# Import the flow creation function and potentially nodes/utils if needed directly
from flow import create_v1_lead_processing_flow
# Assuming pocketflow is installed and accessible
from pocketflow import Flow 

# Configure logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# Secret key needed for flashing messages
app.secret_key = 'your_very_secret_key_here' # Change this in production!

# --- Backend Processing Logic ---

def process_lead_with_flow(lead_info: dict) -> dict:
    """
    Runs the V1 PocketFlow for a single lead and returns the results.
    (Similar to run_single_lead from main.py, adapted for web app context)
    """
    logging.info(f"--- Starting web request processing for lead: {lead_info.get('lead_name', 'N/A')} ---")
    
    # Create a fresh shared store, pre-populated with lead info
    shared_store = lead_info.copy() 
    
    try:
        # Create the flow instance
        # Consider caching the flow creation if it's expensive, but for now, create each time
        v1_flow: Flow = create_v1_lead_processing_flow()
        
        # Run the flow
        v1_flow.run(shared=shared_store)
        
        logging.info(f"--- Finished web request processing for lead: {lead_info.get('lead_name', 'N/A')} ---")
        
        # Extract key results for display 
        # Return the whole shared store for now, template can pick needed fields
        return shared_store

    except Exception as e:
        logging.error(f"Error during PocketFlow execution for lead {lead_info.get('lead_name', 'N/A')}: {e}", exc_info=True)
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
        "lead_name": request.form.get('lead_name', '').strip(),
        "last_name": request.form.get('last_name', '').strip(),
        "company_name": request.form.get('company_name', '').strip(),
        "company_website": request.form.get('company_website', '').strip(),
        "linkedin_url": request.form.get('linkedin_url', '').strip()
    }
    
    # Basic validation (can be more sophisticated)
    if not lead_input['lead_name'] and not lead_input['company_name']:
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