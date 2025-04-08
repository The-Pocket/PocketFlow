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
    conditionally including analysis steps based on flags in initial_shared_data.

    Args:
        initial_shared_data: The initial dictionary containing lead data and
                               enable flags (e.g., 'enable_website_analysis').

    Returns:
        A PocketFlow Flow object representing the V1 workflow.
    """
    logging.info("Creating V1 lead processing flow dynamically...")

    # 1. Extract enable flags and initial data
    enable_website = initial_shared_data.get('enable_website_analysis', False)
    enable_linkedin = initial_shared_data.get('enable_linkedin_analysis', False)
    enable_third_party = initial_shared_data.get('enable_third_party_analysis', False)
    has_initial_website = bool(initial_shared_data.get('company_website'))
    has_initial_linkedin = bool(initial_shared_data.get('linkedin_url'))

    # 2. Instantiate all *potential* nodes
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

    # 3. Build the flow chain conditionally
    current_node = load_lead
    last_node_of_previous_section = load_lead # Keep track for connecting sections

    # --- Website Section ---
    if enable_website:
        logging.info("Website analysis enabled.")
        website_entry_node = scrape_website if has_initial_website else check_website
        logging.info(f"Connecting {current_node.__class__.__name__} -> {website_entry_node.__class__.__name__}")
        last_node_of_previous_section >> website_entry_node

        # Define internal website connections
        if not has_initial_website:
            check_website - "default" >> scrape_website
            # If check fails, where does it connect? Needs to go to the *next enabled* section start
            # We'll handle this connection *after* processing all sections
        
        scrape_website >> analyze_website
        # scrape_website - "scrape_failed" >> ??? # Handle this later
        
        # The last node of this section, if successful
        last_node_of_website = analyze_website
        current_node = last_node_of_website # Update current node for next section connection
    else:
        logging.info("Website analysis disabled.")
        last_node_of_website = last_node_of_previous_section # No change if disabled

    # --- LinkedIn Section ---
    last_node_before_linkedin = current_node # Node to connect *to* linkedin section
    if enable_linkedin:
        logging.info("LinkedIn analysis enabled.")
        linkedin_entry_node = scrape_linkedin if has_initial_linkedin else check_linkedin
        logging.info(f"Connecting {last_node_before_linkedin.__class__.__name__} -> {linkedin_entry_node.__class__.__name__}")
        last_node_before_linkedin >> linkedin_entry_node

        # Define internal linkedin connections
        if not has_initial_linkedin:
            check_linkedin - "default" >> scrape_linkedin
            # check_linkedin - "no_linkedin" >> ??? # Handle this later

        scrape_linkedin >> analyze_linkedin
        # scrape_linkedin - "scrape_failed" >> ??? # Handle this later

        # The last node of this section, if successful
        last_node_of_linkedin = analyze_linkedin
        current_node = last_node_of_linkedin
    else:
        logging.info("LinkedIn analysis disabled.")
        last_node_of_linkedin = last_node_before_linkedin # No change if disabled

    # --- Third Party Section ---
    last_node_before_third_party = current_node
    if enable_third_party:
        logging.info("Third-party analysis enabled.")
        third_party_entry_node = decide_tavily_queries
        logging.info(f"Connecting {last_node_before_third_party.__class__.__name__} -> {third_party_entry_node.__class__.__name__}")
        last_node_before_third_party >> third_party_entry_node

        # Define internal third-party connections
        decide_tavily_queries >> search_third_party
        search_third_party >> analyze_third_party
        # Add failure handling if needed

        # The last node of this section, if successful
        last_node_of_third_party = analyze_third_party
        current_node = last_node_of_third_party
    else:
        logging.info("Third-party analysis disabled.")
        last_node_of_third_party = last_node_before_third_party

    # --- Final Steps Section ---
    last_node_before_final = current_node
    logging.info(f"Connecting {last_node_before_final.__class__.__name__} -> GenerateEmail")
    last_node_before_final >> generate_email
    generate_email >> store_results
    
    # --- Handle Skipped/Failed Section Connections ---
    # Determine the entry point for each section (if enabled)
    linkedin_entry = (scrape_linkedin if has_initial_linkedin else check_linkedin) if enable_linkedin else None
    third_party_entry = decide_tavily_queries if enable_third_party else None
    final_entry = generate_email # Always run final steps for now

    # Define where to go after each potential stopping point if a section is skipped/fails
    next_after_website = linkedin_entry or third_party_entry or final_entry
    next_after_linkedin = third_party_entry or final_entry
    next_after_third_party = final_entry
    
    if enable_website:
        if not has_initial_website:
             logging.info(f"Connecting CheckWebsite['no_website'] -> {next_after_website.__class__.__name__}")
             check_website - "no_website" >> next_after_website
        # Connect scrape failure to the next available section start
        logging.info(f"Connecting ScrapeWebsite['scrape_failed'] -> {next_after_website.__class__.__name__}")
        scrape_website - "scrape_failed" >> next_after_website
        
    if enable_linkedin:
        if not has_initial_linkedin:
             logging.info(f"Connecting CheckLinkedIn['no_linkedin'] -> {next_after_linkedin.__class__.__name__}")
             check_linkedin - "no_linkedin" >> next_after_linkedin
        logging.info(f"Connecting ScrapeLinkedIn['scrape_failed'] -> {next_after_linkedin.__class__.__name__}")
        scrape_linkedin - "scrape_failed" >> next_after_linkedin
        
    # Add connections for decide_tavily_queries/search_third_party failures if needed
    # Example:
    # if enable_third_party:
    #     search_third_party - "search_failed" >> next_after_third_party 

    # 4. Create the Flow object
    v1_flow = Flow(start=load_lead)
    logging.info("V1 lead processing flow created dynamically.")
    
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

