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
    DecideTavilyQueries,
    SearchThirdPartySources,
    AnalyzeThirdPartySources,
    GenerateEmail,
    StoreResults
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_v1_lead_processing_flow(initial_shared_data: dict) -> Flow:
    """
    Creates and connects the nodes for the V1 lead processing workflow,
    conditionally skipping website search if a URL is provided initially.

    Args:
        initial_shared_data: The initial dictionary containing lead data.

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
    decide_tavily_queries = DecideTavilyQueries()
    search_third_party = SearchThirdPartySources()
    analyze_third_party = AnalyzeThirdPartySources()
    generate_email = GenerateEmail()
    store_results = StoreResults()
    # Optional: Define an explicit end node if needed for clarity or specific actions
    # end_node = EndNode() # Assuming an EndNode class exists or is defined

    # 2. Define transitions conditionally based on initial data
    has_initial_website = bool(initial_shared_data.get('company_website'))
    has_initial_linkedin = bool(initial_shared_data.get('linkedin_url'))

    # Determine the node to go to after the website part
    if has_initial_linkedin:
        logging.info("Initial LinkedIn URL provided. Skipping LinkedIn search.")
        next_node_after_website = scrape_linkedin 
    else:
        logging.info("Initial LinkedIn URL not provided. Including LinkedIn search.")
        next_node_after_website = check_linkedin

    # --- Website Branch Logic ---
    if has_initial_website:
        logging.info("Initial company website provided. Skipping website search.")
        # Path: Load -> Scrape Website -> Analyze Website -> (Next Node)
        load_lead >> scrape_website
        scrape_website >> analyze_website
        # scrape_website - "scrape_failed" >> next_node_after_website # Example failure handling
        analyze_website >> next_node_after_website # Connect to LinkedIn check/scrape
    else:
        logging.info("Initial company website not provided. Including website search.")
        # Path: Load -> Check Website -> [Scrape -> Analyze] -> (Next Node)
        load_lead >> check_website
        check_website - "default" >> scrape_website 
        check_website - "no_website" >> next_node_after_website # Skip scrape/analyze
        scrape_website >> analyze_website
        # scrape_website - "scrape_failed" >> next_node_after_website # Example failure handling
        analyze_website >> next_node_after_website # Connect to LinkedIn check/scrape

    # --- LinkedIn Branch Logic ---
    # Define transitions FROM check_linkedin (only relevant if has_initial_linkedin is False)
    check_linkedin - "default" >> scrape_linkedin # Found profile
    check_linkedin - "no_linkedin" >> decide_tavily_queries # Did not find profile

    # Define transitions for the rest of the LinkedIn path
    scrape_linkedin >> analyze_linkedin
    scrape_linkedin - "scrape_failed" >> decide_tavily_queries # Skip analysis on failure
    analyze_linkedin >> decide_tavily_queries

    # --- Third Party Search Path (remains the same) ---
    decide_tavily_queries >> search_third_party
    search_third_party >> analyze_third_party
    analyze_third_party >> generate_email 

    # --- Final steps (remains the same) ---
    generate_email >> store_results
    # store_results >> end_node 

    # 3. Create the Flow object, starting with the first node
    v1_flow = Flow(start=load_lead)
    logging.info("V1 lead processing flow created successfully.")
    
    return v1_flow

if __name__ == '__main__':
    # Example of creating the flow (actual execution would happen in main.py)
    # This example won't reflect the conditional logic as it needs initial_shared_data
    print("\nFlow creation function defined. Run main.py for execution examples.")
    # Example instantiation (requires dummy data)
    # dummy_data_with_site = {'company_website': 'exists.com'}
    # flow_with_site = create_v1_lead_processing_flow(dummy_data_with_site)
    # print(f"Flow (with site) start node: {flow_with_site.start_node.__class__.__name__}") 
    # # You'd need more inspection logic to see the *actual* next node connection here

    # dummy_data_no_site = {}
    # flow_no_site = create_v1_lead_processing_flow(dummy_data_no_site)
    # print(f"Flow (no site) start node: {flow_no_site.start_node.__class__.__name__}")

