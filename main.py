"""Main entry point for testing the V1 lead processing flow."""

import logging
import json

from flow import create_v1_lead_processing_flow

# Configure logging same as other modules
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_single_lead(lead_info: dict):
    """Runs the V1 flow for a single lead's data."""
    logging.info(f"--- Starting processing for lead: {lead_info.get('lead_name', 'N/A')} ---")
    
    # Create a fresh shared store for this run, pre-populated with lead info
    shared_store = lead_info.copy() # Start with lead info
    
    # Create the flow instance
    v1_flow = create_v1_lead_processing_flow()
    
    # Run the flow - initial data is already in shared_store
    # The first node (LoadLeadData) will now mostly just initialize placeholders
    v1_flow.run(shared=shared_store)
    
    logging.info(f"--- Finished processing for lead: {lead_info.get('lead_name', 'N/A')} ---")
    
    # Print the final state of the shared store for inspection
    print("\nFinal Shared Store State:")
    print(json.dumps(shared_store, indent=2, default=str)) # Use default=str for non-serializable items if any
    print("---------------------------")
    return shared_store

if __name__ == "__main__":
    # --- Test Case 1: Lead with Website and LinkedIn ---
    lead1 = {
        "lead_name": "Alice",
        "last_name": "Smith",
        "company_name": "Innovate Solutions",
        "company_website": "https://innovate-solutions.example",
        "linkedin_url": "https://linkedin.com/in/alice-smith-example"
    }
    run_single_lead(lead1)

    # --- Test Case 2: Lead with only Website ---
    lead2 = {
        "lead_name": "Bob",
        "last_name": "Jones",
        "company_name": "Global Tech",
        "company_website": "https://global-tech.example",
        "linkedin_url": None # Explicitly None
    }
    # run_single_lead(lead2) # Uncomment to run

    # --- Test Case 3: Lead with only LinkedIn ---
    lead3 = {
        "lead_name": "Charlie",
        "last_name": "Brown",
        "company_name": "Synergy Corp",
        "company_website": "", # Empty string
        "linkedin_url": "https://linkedin.com/in/charlie-brown-example"
    }
    # run_single_lead(lead3) # Uncomment to run

    # --- Test Case 4: Lead with No Website or LinkedIn ---
    lead4 = {
        "lead_name": "David",
        "last_name": "Williams",
        "company_name": "Acme Inc.",
        "company_website": None,
        "linkedin_url": ""
    }
    # run_single_lead(lead4) # Uncomment to run 