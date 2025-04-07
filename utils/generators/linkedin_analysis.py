"""Generate analysis for LinkedIn profile content."""

import logging
from typing import Optional
from utils.ai import call_llm

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_linkedin_analysis(lead_name: str, company_name: str, linkedin_url: str, linkedin_content: str, model: Optional[str] = None) -> str:
    """
    Generate a detailed analysis of a LinkedIn profile.

    Args:
        lead_name: Name of the lead
        company_name: Name of the company
        linkedin_url: URL of the LinkedIn profile
        linkedin_content: Scraped content from LinkedIn (should be formatted text)
        model: Optional specific model identifier to use.

    Returns:
        Structured analysis of the LinkedIn profile, or an error string.
    """
    # Craft the prompt for LinkedIn analysis
    prompt = f"""
You are an expert sales intelligence analyst. Create a detailed analysis of {lead_name}'s LinkedIn profile at {company_name}.

LINKEDIN CONTENT:
URL: {linkedin_url}

{linkedin_content[:15000]}  # Limit content length

Based on this LinkedIn content, create a comprehensive analysis with three distinct sections:

1. PROFESSIONAL SNAPSHOT: Summarize their career history, skills, and notable achievements.
2. OUTREACH ANGLES: Identify 2-3 specific points from their profile that could serve as effective conversation starters or sales angles.
3. UNIQUE CONNECTOR: Find one truly unique detail about them that could serve as a personal connection point (e.g., shared alma mater, mutual interest, recent achievement).

Format your response with clear section headers and concise, actionable points in each section.
"""

    logging.info(f"Calling LLM to generate LinkedIn analysis for {lead_name} at {company_name}")
    analysis = call_llm(
        prompt=prompt,
        model=model,
        temperature=0.5,
        max_tokens=1000
    )

    if isinstance(analysis, str) and analysis.startswith("ERROR:"):
        logging.error(f"Failed to generate LinkedIn analysis: {analysis}")
        return analysis # Return the error string
    elif isinstance(analysis, str):
        logging.info(f"Generated LinkedIn analysis for {lead_name} at {company_name} ({len(analysis)} chars)")
        return analysis
    else:
        # Should not happen if json_mode=False, but handle defensively
        logging.error("Unexpected return type from call_llm for LinkedIn analysis")
        return "Error: Unexpected response format from LLM"

if __name__ == '__main__':
    # Example usage for testing
    print("\n--- Testing LinkedIn Analysis Generator --- (Requires .env)")
    test_lead = "Jane Doe"
    test_company = "Innovate Inc."
    test_url = "https://linkedin.com/in/janedoe"
    test_content = """
    PROFILE INFORMATION
    Name: Jane Doe
    Title: Senior Software Engineer at Innovate Inc.
    Location: San Francisco Bay Area
    Summary: Experienced software engineer passionate about building scalable web applications.

    WORK EXPERIENCE
    - Senior Software Engineer at Innovate Inc. (2020-Present)
      Description: Lead development on key projects.
    - Software Engineer at Tech Solutions (2018-2020)
      Description: Developed backend services.

    EDUCATION
    - Stanford University, M.S. in Computer Science (2016-2018)
    - UC Berkeley, B.S. in Electrical Engineering and Computer Sciences (2012-2016)

    SKILLS
    - Python
    - Java
    - Cloud Computing
    """
    
    print(f"Lead: {test_lead}, Company: {test_company}, URL: {test_url}")
    # Test with default model
    print("\n--- Testing with Default Model ---")
    result_default = generate_linkedin_analysis(test_lead, test_company, test_url, test_content)
    print("\nAnalysis Report (Default):")
    print(result_default)
    
    # Example of testing with a specific model (uncomment if needed and keys are set)
    # print("\n--- Testing with Specific Model (e.g., gemini-1.5-pro-latest) ---")
    # result_specific = generate_linkedin_analysis(test_lead, test_company, test_url, test_content, model="gemini-1.5-pro-latest")
    # print("\nAnalysis Report (Specific):")
    # print(result_specific)

    print("\n-------------------------------------------") 