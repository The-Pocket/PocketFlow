"""Defines the PocketFlow flow for the V1 lead processing workflow."""

import logging
from pocketflow import Flow

# Import node classes
from nodes import (
    LoadLeadData,
    CheckWebsiteExists,
    ScrapeWebsite,
    AnalyzeWebsite,
    CheckLinkedInExists,
    ScrapeLinkedIn,
    AnalyzeLinkedIn,
    GenerateEmail,
    StoreResults
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_v1_lead_processing_flow() -> Flow:
    """
    Creates and connects the nodes for the V1 lead processing workflow.

    Returns:
        A PocketFlow Flow object representing the V1 workflow.
    """
    logging.info("Creating V1 lead processing flow...")

    # 1. Instantiate all nodes
    load_lead = LoadLeadData()
    check_website = CheckWebsiteExists()
    scrape_website = ScrapeWebsite()
    analyze_website = AnalyzeWebsite()
    check_linkedin = CheckLinkedInExists()
    scrape_linkedin = ScrapeLinkedIn()
    analyze_linkedin = AnalyzeLinkedIn()
    generate_email = GenerateEmail()
    store_results = StoreResults()
    # Optional: Define an explicit end node if needed for clarity or specific actions
    # end_node = EndNode() # Assuming an EndNode class exists or is defined

    # 2. Define transitions based on the diagram and node design
    load_lead >> check_website

    # Website branch
    check_website - "has_website" >> scrape_website
    scrape_website >> analyze_website
    analyze_website >> check_linkedin # Both website paths converge here

    # No website path
    check_website - "no_website" >> check_linkedin # Skip website steps

    # LinkedIn branch
    check_linkedin - "has_linkedin" >> scrape_linkedin
    scrape_linkedin >> analyze_linkedin
    analyze_linkedin >> generate_email # Both LinkedIn paths converge here

    # No LinkedIn path
    check_linkedin - "no_linkedin" >> generate_email # Skip LinkedIn steps

    # Final steps
    generate_email >> store_results
    # If using an explicit end node:
    # store_results >> end_node 
    
    # 3. Create the Flow object, starting with the first node
    v1_flow = Flow(start=load_lead)
    logging.info("V1 lead processing flow created successfully.")
    
    return v1_flow

if __name__ == '__main__':
    # Example of creating the flow (actual execution would happen in main.py)
    flow = create_v1_lead_processing_flow()
    print("\nFlow created. Details:")
    # You might add a way to visualize or print transitions if PocketFlow supports it,
    # otherwise, this just confirms the function runs.
    # For example (conceptual):
    # print(flow.get_transitions())
    print(f"Start node: {flow.start_node.__class__.__name__}")
    # Add more prints to inspect node connections if needed for debugging

