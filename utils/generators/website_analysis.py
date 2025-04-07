"""Generate analysis for website content."""

import logging
from typing import Optional
from utils.ai import call_llm

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_website_analysis(company_name: str, website_url: str, website_content: str, model: Optional[str] = None) -> str:
    """
    Generate a detailed analysis of a company website using a specialist prompt.

    Args:
        company_name: Name of the company
        website_url: URL of the company website
        website_content: Scraped content from the website
        model: Optional specific model identifier to use.

    Returns:
        Structured analysis report of the company website, or an error string.
    """
    # Limit content length before putting it in the prompt
    max_content_length = 15000
    if len(website_content) > max_content_length:
        logging.info(f"Truncating website content from {len(website_content)} to {max_content_length} chars for analysis prompt")
        website_content = website_content[:max_content_length]
        
    # Craft the new prompt structure
    prompt = f"""You are a website analysis specialist who extracts hidden business insights from company websites.

Website URL being analyzed: {website_url}
Company Name: {company_name}

## ANALYSIS PRIORITIES
1. Identify their core value proposition and target audience
2. Extract key service/product offerings and specializations
3. Find evidence of their positioning strategy and differentiation
4. Uncover client types, case studies, and success metrics
5. Detect messaging around pain points they solve for clients

## WEBSITE CONTENT TO ANALYZE:
```
{website_content}
```

## OUTPUT FORMAT
Please generate a report using the following structure:

**Detailed Website Analysis Report: {company_name}**
**Report Prepared For:** Sales Team

**Objective:** To provide a detailed analysis of {company_name} based on their website data to equip the sales team with actionable insights for engaging and potentially collaborating with them.

**Executive Summary:**
[2-3 sentences capturing the essence of the company's positioning and key differentiators based *only* on the provided website content.]

**Deep Dive Analysis of {company_name} Website Data:**

**1. Core Value Proposition & Target Audience:**
- [Specific audience targeting evidence found on the site]
- [Key messaging that reveals their positioning according to the site]
- [Evidence of specialization or focus mentioned on the site]

**2. Key Service Areas & Specializations:**
- [Detailed breakdown of services/products mentioned, emphasizing prominent ones]
- [Technical capabilities or expertise highlighted on the site]

**3. Client Success Indicators:**
- [Case study themes and results emphasized on the site]
- [Client types or industries highlighted on the site]
- [Success metrics featured on the site]

**4. Insights and Things Not Explicitly Said But Hinted At:**
- [Inferences about market positioning based *only* on website content]
- [Potential ideal client profile suggested by the website]
- [Technology or methodology preferences hinted at on the site]
- [Possible gaps in their service offerings based on what's *not* mentioned relative to stated goals]

**Recommendations for the Sales Team (Based ONLY on Website Data):**
- [3-5 specific, actionable conversation starters derived from website findings]
- [Value alignment opportunities suggested by website content]
- [Differentiation points (from website) to emphasize in outreach]

**Conclusion:**
[Summary of strongest selling angles derived strictly from the website and suggested next steps for sales based on this analysis.]

**IMPORTANT GUIDELINES:**
- Base your entire analysis strictly on the provided website content.
- Extract specific language and terminology they use.
- Note which services/products get the most prominent placement.
- Identify any patterns in their case studies or client testimonials.
- Look for recent changes or updates if mentioned.
- Pay attention to calls-to-action and contact emphasis.
- Focus on specific, actionable insights rather than general observations.
"""

    logging.info(f"Calling LLM to generate website analysis for {company_name} using specialist prompt")
    analysis = call_llm(
        prompt=prompt,
        model=model, # Pass through optional model override
        temperature=0.5, # Lower temp for more focused analysis
        max_tokens=2000 # Allow for a longer, more detailed report
    )

    if isinstance(analysis, str) and analysis.startswith("ERROR:"):
        logging.error(f"Failed to generate website analysis: {analysis}")
        return analysis # Return the error string
    elif isinstance(analysis, str):
        logging.info(f"Generated website analysis for {company_name} ({len(analysis)} chars)")
        return analysis
    else:
        logging.error("Unexpected return type from call_llm for website analysis")
        return "Error: Unexpected response format from LLM"

if __name__ == '__main__':
    # Example usage for testing
    print("\n--- Testing Website Analysis Generator (Specialist Prompt) --- (Requires .env)")
    test_company = "Example Corp"
    test_url = "https://example.com"
    test_content = "Example Corp provides innovative solutions for complex problems. We target enterprise customers in the finance sector. Our unique value proposition is our patented algorithm. Check out our case study with BigBank showing 30% ROI. Contact us today for a demo! Our services include AlgoTrading Platform and Risk Analysis Suite."
    
    print(f"Company: {test_company}, URL: {test_url}")
    # Test with default model
    print("\n--- Testing with Default Model ---")
    result_default = generate_website_analysis(test_company, test_url, test_content)
    print("\nAnalysis Report (Default):")
    print(result_default)
    
    # Example of testing with a specific model (uncomment if needed and keys are set)
    # print("\n--- Testing with Specific Model (e.g., gemini-1.5-pro-latest) ---")
    # result_specific = generate_website_analysis(test_company, test_url, test_content, model="gemini-1.5-pro-latest")
    # print("\nAnalysis Report (Specific):")
    # print(result_specific)
    
    print("\n-------------------------------------------") 