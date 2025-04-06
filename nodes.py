# nodes.py

import logging
import re # For basic URL validation
import json
import datetime # Make sure datetime is imported

from pocketflow import Node
# Ensure these imports are present at the top
from utils.ai_analyzer import call_llm_text_output, call_llm_with_json_output
from utils import database, web_scraper, linkedin_scraper, search, ai_generator

class LoadLeadData(Node):
    """Initial node to load lead data from input parameters."""
    def prep(self, shared):
        """Nothing to prepare, just access the initial input data."""
        return None
        
    def exec(self, prep_res):
        """No computation needed, just pass through."""
        return None
    
    def post(self, shared, prep_res, exec_res):
        """Validate required fields exist in shared data."""
        required_fields = ['lead_name', 'company_name']
        
        # Log what we found
        for field in required_fields:
            if field not in shared or not shared[field]:
                logging.warning(f"Required field '{field}' missing or empty in lead data.")
                return "error"  # Potentially handle error path
        
        logging.info(f"Loaded lead data: {shared['lead_name']} from {shared['company_name']}")
        return "default"  # Proceed to next node (CheckWebsiteExists)

class CheckWebsiteExists(Node):
    """Checks if a valid website URL is provided."""
    def prep(self, shared):
        """Extract website URL from shared data."""
        return shared.get("company_website")
        
    def exec(self, website_url):
        """Basic check if URL is non-empty and well-formed."""
        if isinstance(website_url, str) and website_url.strip():
            # Simple regex to check if it's a reasonably valid URL
            url_pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
            if url_pattern.match(website_url):
                logging.info(f"Valid website URL found: {website_url}")
                return True
        logging.info("No valid website URL found.")
        return False
    
    def post(self, shared, prep_res, exec_res):
        """Returns action based on website availability."""
        return "has_website" if exec_res else "no_website"

class ScrapeWebsite(Node):
    """Scrapes a website using Firecrawl service."""
    def prep(self, shared):
        """Extracts the website URL from shared."""
        website_url = shared.get("company_website")
        if not website_url:
            logging.warning("No company website URL provided for scraping.")
            return None
        return website_url
        
    def exec(self, prep_res):
        """Calls the Firecrawl service to scrape website content."""
        if prep_res is None:
            return "Error: No valid URL to scrape."
            
        url = prep_res
        try:
            logging.info(f"Scraping website content from {url}")
            result = web_scraper.call_firecrawl(url)
            return result
        except Exception as e:
            logging.error(f"Error scraping website: {str(e)}")
            return f"Error: {str(e)}"
            
    def post(self, shared, prep_res, exec_res):
        """Stores the scraped website content."""
        shared["website_content"] = exec_res
        if isinstance(exec_res, str) and exec_res.startswith("Error:"):
            logging.warning(f"Website scraping failed: {exec_res}")
        else:
            logging.info("Stored scraped website content.")
        return "default"  # Proceed to AnalyzeWebsite

class AnalyzeWebsite(Node):
    """Analyzes website content using a detailed prompt."""
    def prep(self, shared):
        """Packages required content for analysis."""
        website_content = shared.get("website_content")
        if not website_content:
            logging.warning("No website content available for analysis.")
            return None
            
        # Prepare the context dictionary
        context = {
            "raw_content": website_content,
            "lead_name": shared.get("lead_name", "Unknown"),
            "company_name": shared.get("company_name", "Unknown Company"),
            "website_url": shared.get("company_website", "")
        }
        return context
        
    def exec(self, prep_res):
        """Calls LLM with website analysis prompt."""
        if prep_res is None:
            return "Error: No valid website content to analyze."
            
        website_text = prep_res["raw_content"]
        lead_name = prep_res["lead_name"]
        company_name = prep_res["company_name"]
        website_url = prep_res["website_url"]
        
        # Limit input length to avoid excessive token usage
        max_input_length = 15000 
        if len(website_text) > max_input_length:
            logging.warning(f"Website text truncated to {max_input_length} characters for analysis.")
            website_text = website_text[:max_input_length]
        
        import datetime
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Build prompt using string concatenation instead of f-string to avoid indentation issues
        website_analysis_prompt = "You are a website analysis specialist who extracts hidden business insights from company websites.\n\n"
        website_analysis_prompt += f"The lead information is:\n"
        website_analysis_prompt += f"name - {lead_name}\n"
        website_analysis_prompt += f"Company - {company_name}\n"
        website_analysis_prompt += f"website url - {website_url}\n"
        website_analysis_prompt += f"- Analysis Date: {current_date}\n\n"
        
        website_analysis_prompt += "## WEBSITE CONTENT TO ANALYZE\n"
        website_analysis_prompt += f"\"\"\"\n{website_text}\n\"\"\"\n\n"
        
        website_analysis_prompt += "## ANALYSIS PRIORITIES\n"
        website_analysis_prompt += "1. Identify their core value proposition and target audience\n"
        website_analysis_prompt += "2. Extract key service/product offerings and specializations\n"
        website_analysis_prompt += "3. Find evidence of their positioning strategy and differentiation\n"
        website_analysis_prompt += "4. Uncover client types, case studies, and success metrics\n"
        website_analysis_prompt += "5. Detect messaging around pain points they solve for clients\n\n"
        
        website_analysis_prompt += "## OUTPUT FORMAT\n"
        website_analysis_prompt += f"**Detailed Lead Analysis Report: {company_name} - {lead_name}**\n"
        website_analysis_prompt += f"**Date:** {current_date}\n"
        website_analysis_prompt += f"**Time:** {current_time}\n"
        website_analysis_prompt += "**Report Prepared For:** Sales Team\n\n"
        
        website_analysis_prompt += f"**Objective:** To provide a detailed analysis of {company_name} based on their website data to equip the sales team with actionable insights for engaging and potentially collaborating with them.\n\n"
        
        website_analysis_prompt += "**Executive Summary:**\n"
        website_analysis_prompt += "[2-3 sentences capturing the essence of the company's positioning and key differentiators based *only* on the website content provided.]\n\n"
        
        website_analysis_prompt += f"**Deep Dive Analysis of {company_name} Website Data:**\n\n"
        
        website_analysis_prompt += "**1. Core Value Proposition & Target Audience:**\n"
        website_analysis_prompt += "- [Specific audience targeting evidence from website]\n"
        website_analysis_prompt += "- [Key messaging that reveals their positioning from website]\n"
        website_analysis_prompt += "- [Evidence of specialization or focus from website]\n\n"
        
        website_analysis_prompt += "**2. Key Service Areas & Specializations:**\n"
        website_analysis_prompt += "- [Detailed breakdown of services/products mentioned on website with emphasis on priority areas]\n"
        website_analysis_prompt += "- [Technical capabilities or expertise highlighted on website]\n\n"
        
        website_analysis_prompt += "**3. Client Success Indicators:**\n"
        website_analysis_prompt += "- [Case study themes and results emphasized on website]\n"
        website_analysis_prompt += "- [Client types or industries they highlight on website]\n"
        website_analysis_prompt += "- [Success metrics they choose to feature on website]\n\n"
        
        website_analysis_prompt += "**4. Insights and Things Not Explicitly Said But Hinted At (Based *only* on website content):**\n"
        website_analysis_prompt += "- [Market positioning inferences from website]\n"
        website_analysis_prompt += "- [Potential ideal client profile based on website messaging]\n"
        website_analysis_prompt += "- [Technology or methodology preferences hinted at on website]\n"
        website_analysis_prompt += "- [Possible gaps in their service offerings based on what's *not* mentioned prominently]\n\n"
        
        website_analysis_prompt += "**Recommendations for the Sales Team (Based *only* on website content):**\n"
        website_analysis_prompt += "- [3-5 specific, actionable conversation starters referencing website details]\n"
        website_analysis_prompt += "- [Value alignment opportunities suggested by website content]\n"
        website_analysis_prompt += "- [Differentiation points to emphasize based on website content]\n\n"
        
        website_analysis_prompt += "**Conclusion:**\n"
        website_analysis_prompt += "[Summary of strongest selling angles based *only* on website and potential next steps]\n\n"
        
        website_analysis_prompt += "Focus on specific, actionable insights rather than general observations.\n\n"
        
        website_analysis_prompt += "IMPORTANT GUIDELINES:\n"
        website_analysis_prompt += "- Extract specific language and terminology they use (this indicates their priorities)\n"
        website_analysis_prompt += "- Note which services/products get the most prominent placement\n"
        website_analysis_prompt += "- Identify any patterns in their case studies or client testimonials\n"
        website_analysis_prompt += "- Look for recent changes or updates (new service offerings, etc.)\n"
        website_analysis_prompt += "- Pay attention to calls-to-action and what they emphasize in contact forms\n"

        # Call LLM and handle errors
        try:
            logging.info("Calling LLM (gpt-4o) for Website Analysis")
            analysis_report_text = call_llm_text_output(
                prompt=website_analysis_prompt, 
                purpose="Detailed Website Analysis",
                model_name="gpt-4o"
            )
            
            if analysis_report_text is not None:
                return analysis_report_text
            else:
                return "Error: Failed to generate website analysis report."
        except Exception as e:
            logging.error(f"Website analysis error: {str(e)}")
            return f"Error: {str(e)}"

    def post(self, shared, prep_res, exec_res):
        """Stores the analysis report string (or error string)."""
        shared["website_report"] = exec_res 
        if isinstance(exec_res, str) and exec_res.startswith("Error:"): 
            logging.warning(f"Website analysis failed: {exec_res}")
        else:
            logging.info("Stored website analysis report.")
        return "default" # Proceed to CheckLinkedInExists

class CheckLinkedInExists(Node):
    """Checks if a potentially valid LinkedIn URL is provided."""
    def prep(self, shared):
        return shared.get("linkedin_url")

    def exec(self, linkedin_url):
        """Basic check if URL is non-empty string and contains 'linkedin.com'"""
        if isinstance(linkedin_url, str) and linkedin_url.strip():
            # Simple check, could be more robust
            if "linkedin.com" in linkedin_url.lower():
                 logging.info(f"LinkedIn URL found: {linkedin_url}")
                 return True
        logging.info("No valid LinkedIn URL found.")
        return False

    def post(self, shared, prep_res, exec_res):
        """Returns action based on whether a valid URL was found."""
        return "has_linkedin" if exec_res else "no_linkedin"

class ScrapeLinkedIn(Node):
    """Calls the utility to scrape LinkedIn profile data."""
    def prep(self, shared):
        return shared.get("linkedin_url") # Should exist if we reached here

    def exec(self, url):
        logging.info(f"Initiating LinkedIn profile scrape for: {url}")
        return linkedin_scraper.call_apify_linkedin_profile(url)

    def post(self, shared, prep_res, exec_res):
        """Stores the scraped profile data (or error dict)."""
        shared["linkedin_raw_profile"] = exec_res
        if isinstance(exec_res, dict) and exec_res.get("error"):
            logging.warning(f"LinkedIn scraping failed: {exec_res['error']}")
        else:
            logging.info("Stored LinkedIn raw profile data.")
        return "default" # Proceed to AnalyzeLinkedIn

class AnalyzeLinkedIn(Node):
    """Analyzes scraped LinkedIn profile data using the Sales Intelligence specialist prompt."""
    def prep(self, shared):
        # Need more than just raw_profile for the new prompt
        return {
            "raw_profile": shared.get("linkedin_raw_profile"),
            "lead_name": f"{shared.get('lead_name', '')} {shared.get('last_name', '')}".strip(),
            "company_name": shared.get("company_name"),
            "linkedin_url": shared.get("linkedin_url")
        }

    def exec(self, prep_res):
        raw_profile = prep_res.get("raw_profile")
        lead_name = prep_res.get("lead_name", 'N/A')
        company_name = prep_res.get("company_name", 'N/A')
        linkedin_url = prep_res.get("linkedin_url", 'N/A')

        if not raw_profile or (isinstance(raw_profile, dict) and raw_profile.get("error")):
            logging.warning("Skipping LinkedIn analysis due to missing or error data.")
            # Return an error string, as the output is now text
            return "Error: No valid LinkedIn profile data to analyze"

        # Serialize profile data for the prompt (assuming the prompt *should* use it)
        try:
            profile_text = json.dumps(raw_profile, indent=2)
            # Limit input length
            max_input_length = 15000
            if len(profile_text) > max_input_length:
                logging.warning(f"LinkedIn profile text truncated to {max_input_length} characters for analysis.")
                profile_text = profile_text[:max_input_length]
        except TypeError:
            logging.warning("Could not serialize profile data to JSON for LLM prompt.")
            return "Error: Could not serialize profile data for LLM prompt"

        current_date = datetime.datetime.now().strftime("%Y-%m-%d") # Date format for prompt

        # Use the new Sales Intelligence specialist prompt for LinkedIn
        linkedin_sales_prompt = f"""You are a sales intelligence specialist analyzing LinkedIn profile data.
Your task is to extract only the most relevant insights that would help in personalized outreach.

if no information found return no information received after scraping

## ANALYSIS FOCUS
1. Extract core professional data:
   - Name, current role, and company
   - Specific technical skills that indicate decision-making areas

2. Identify actionable sales angles:
   - Look for recent skill acquisitions or certifications
   - Note specific technology affiliations that suggest buying authority
   - Identify career trajectory patterns that indicate priorities

3. Determine relationship leverage points:
   - Find unusual or distinctive aspects of their background
   - Identify specific achievements or projects they might take pride in
   - Note endorsement patterns that reveal professional reputation

## INPUT DATA
```json
{profile_text}
```

## OUTPUT FORMAT
Create a concise profile with these sections:

1. PROFESSIONAL SNAPSHOT (2-3 bullet points)
   - Current role and responsibilities (as specifically as possible)
   - Technical specializations that indicate buying influence
   - Career trajectory insights

2. OUTREACH ANGLES (2-3 bullet points)
   - Specific technologies they work with
   - Projects or achievements worth mentioning
   - Certifications or specializations that suggest needs

3. UNIQUE CONNECTOR (1 specific detail)
   - One distinctive element that sets them apart
   - Something specific enough to demonstrate genuine interest

Focus on quality insights over comprehensive details.

IMPORTANT: Don't make assumptions or add information not present in the data. If information is unavailable, note its absence rather than filling gaps with speculation.
"""
        logging.info("Initiating LinkedIn profile analysis with LLM (gpt-4o-mini) using Sales Intelligence specialist prompt.")
        # <<< USE TEXT OUTPUT FUNCTION >>>
        analysis_result_text = call_llm_text_output(
            prompt=linkedin_sales_prompt,
            purpose="LinkedIn Sales Intelligence Analysis",
            model_name="gpt-4o-mini" # <-- Specify model
        )
        # Return the text report, or an error string
        return analysis_result_text if analysis_result_text is not None else "Error: Failed to generate LinkedIn sales intelligence analysis."

    def post(self, shared, prep_res, exec_res):
        """Stores the analysis report string (or error string)."""
        # <<< STORE TEXT REPORT >>>
        shared["linkedin_report"] = exec_res # exec_res is now a string or None/Error string
        if isinstance(exec_res, str) and exec_res.startswith("Error:"):
            logging.warning(f"LinkedIn analysis failed or returned error: {exec_res}")
        elif exec_res is None:
             logging.error(f"LinkedIn analysis failed unexpectedly (returned None).")
             shared["linkedin_report"] = "Error: LinkedIn analysis failed unexpectedly."
        else:
            logging.info("Stored LinkedIn analysis report text.")
        # This node's output doesn't affect the main flow path decision here
        return "default" # Proceed to DecideTavilyQueries

class DecideTavilyQueries(Node):
    """Uses an LLM to generate targeted Tavily search queries."""
    def prep(self, shared):
        """Prepare context for the query generation prompt."""
        company_name = shared.get('company_name')
        lead_name = f"{shared.get('lead_name', '')} {shared.get('last_name', '')}".strip()
        
        if not company_name and not (lead_name and lead_name != shared.get('lead_name', '')): 
             logging.warning("Cannot generate Tavily queries without Company Name or Full Lead Name.")
             return None
        
        logging.info("Preparing context for AI query generation.")
        return {
            "company_name": company_name,
            "full_name": lead_name if lead_name else None
        }
        
    def exec(self, prep_res):
        """Calls LLM to generate a list of search queries."""
        if prep_res is None:
             return {"error": "Insufficient info for query generation."}
             
        company_name = prep_res["company_name"]
        full_name = prep_res["full_name"]
        
        query_gen_prompt = f"""
You are a research assistant tasked with generating effective search queries for the Tavily search API to gather third-party intelligence about a company and potentially a specific person at that company. Do not include queries for the company's own website or LinkedIn.

Company Name: "{company_name}"
Lead's Full Name: "{full_name if full_name else 'N/A'}"

Generate a JSON list containing 4 diverse and targeted search query strings based on these strategies:
1.  **Company News/Reports:** Find recent news, funding, partnerships, or mentions in industry reports.
2.  **Company Reviews/Sentiment:** Look for reviews on third-party sites (like G2, Capterra) or discussions (like Reddit).
3.  **Lead's External Presence (if name provided):** Find conference appearances, podcast interviews, or articles authored by the lead.
4.  **Competitive/Market Context:** Find analysis or comparisons mentioning the company.

Example good queries:
- "{company_name} mentioned in Gartner report"
- "{company_name} customer reviews site:g2.com"
- "{full_name} speaker at SaaStr conference"
- "{company_name} funding announcement 2024"

Output ONLY the JSON list of strings. Example: ["query1", "query2", "query3", "query4"]
"""

        logging.info(f"Calling LLM (gpt-4o-mini) to generate Tavily queries.")
        # Specify the model directly
        result = call_llm_with_json_output(
            prompt=query_gen_prompt, 
            purpose="Tavily Query Generation",
            model_name="gpt-4o-mini" # <--- Specify model
        )
        
        if isinstance(result, list) and all(isinstance(q, str) for q in result):
             logging.info(f"LLM generated {len(result)} queries successfully.")
             return result
        elif isinstance(result, dict) and result.get("error"):
             logging.error(f"LLM call failed during query generation: {result['error']}")
             return {"error": result['error']}
        else:
             logging.error(f"Unexpected result format from LLM: {type(result)}")
             return {"error": "Invalid format returned by LLM for query generation."}
             
    def post(self, shared, prep_res, exec_res):
        """Stores the generated search queries."""
        if isinstance(exec_res, dict) and exec_res.get("error"):
             # Store error message 
             shared["query_generation_error"] = exec_res["error"]
             # Store empty queries list (fallback)
             shared["ai_generated_tavily_queries"] = []
             logging.warning(f"Tavily query generation failed: {exec_res['error']}")
        else:
             # Store the list of generated queries
             shared["ai_generated_tavily_queries"] = exec_res
             shared["query_generation_error"] = None
             logging.info(f"Generated {len(exec_res)} Tavily search queries.")
             
        return "default" # Proceed to SearchThirdPartySources

class SearchThirdPartySources(Node):
    """Searches third-party sources using the AI-generated Tavily queries."""
    def prep(self, shared):
        """Gathers the generated queries to use."""
        return shared.get("ai_generated_tavily_queries", [])
        
    def exec(self, queries):
        """Calls Tavily search with the queries."""
        if not queries:
            logging.warning("No valid Tavily search queries available.")
            return []
            
        # Limit the maximum number of queries to execute
        max_queries = 3 # Can be adjusted
        if len(queries) > max_queries:
            logging.info(f"Limiting Tavily searches to {max_queries} out of {len(queries)} generated queries.")
            queries = queries[:max_queries]
            
        # Execute searches and collect results
        results = []
        seen_urls = set() # Track URLs to deduplicate results
        
        for query in queries:
            logging.info(f"Executing Tavily search: {query}")
            try:
                search_result = search.call_tavily_search(query)
                if search_result and not search_result.get("error"):
                    # Extract and deduplicate the result snippets
                    for item in search_result.get("results", []):
                        if item.get("url") and item.get("url") not in seen_urls:
                            seen_urls.add(item.get("url"))
                            # Add query that found this result for context
                            item["source_query"] = query
                            results.append(item)
                else:
                    logging.warning(f"Tavily search failed for query '{query}': {search_result.get('error', 'Unknown error')}")
            except Exception as e:
                logging.error(f"Exception during Tavily search for '{query}': {str(e)}")
                
        logging.info(f"Collected {len(results)} unique results from {len(queries)} Tavily searches.")
        return results
            
    def post(self, shared, prep_res, exec_res):
        """Stores the search results."""
        shared["third_party_search_results"] = exec_res
        if not exec_res:
            logging.warning("No third-party search results found.")
        else:
            logging.info(f"Stored {len(exec_res)} third-party search results.")
        return "default" # Proceed to AnalyzeThirdPartySources

class AnalyzeThirdPartySources(Node):
    """Analyzes Tavily search results using strategic business analyst prompt."""
    
    def prep(self, shared):
        """Prepare context for third-party source analysis."""
        search_results = shared.get("third_party_search_results", [])
        if not search_results:
            logging.warning("No third-party search results found for analysis.")
            return None
            
        # Extract relevant context from the shared store
        lead_name = shared.get("lead_name", "Unknown")
        company_name = shared.get("company_name", "Unknown Company")
        
        return {
            "search_results": search_results,
            "lead_name": lead_name,
            "company_name": company_name
        }
        
    def exec(self, prep_res):
        """Call LLM to analyze third-party sources."""
        if prep_res is None:
            return "Error: No third-party search results available to analyze."
            
        # Extract context
        search_results = prep_res["search_results"]
        lead_name = prep_res["lead_name"]
        company_name = prep_res["company_name"]
        
        # Process search results into text chunks
        source_snippets = []
        for i, result in enumerate(search_results, 1):
            snippet = f"Source {i}: {result.get('title', 'Untitled')}\nURL: {result.get('url', 'No URL')}\nContent: {result.get('content', 'No content')}"
            source_snippets.append(snippet)
            
        all_sources_text = "\n\n".join(source_snippets)
        
        import datetime
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Build the strategic analyst prompt using string concatenation
        strategy_prompt = "# ROLE: Strategic Business Analyst\n\n"
        strategy_prompt += "You are a strategic business analyst providing precision intelligence on companies and market opportunities.\n\n"
        
        strategy_prompt += "## CONTEXT:\n"
        strategy_prompt += f"You are analyzing information about {company_name} for our sales representative who is preparing to meet with {lead_name}.\n"
        strategy_prompt += f"Date of Analysis: {current_date}\n\n"
        
        strategy_prompt += "## SOURCE INFORMATION:\n"
        strategy_prompt += all_sources_text + "\n\n"
        
        strategy_prompt += "## ANALYSIS REQUIREMENTS:\n"
        strategy_prompt += "1. Synthesize the third-party information into strategic insights\n"
        strategy_prompt += "2. Identify the company's business model, target market, and unique value proposition\n"
        strategy_prompt += "3. Uncover potential pain points or opportunities for collaboration\n"
        strategy_prompt += "4. Assess competitive positioning and market trajectory\n"
        strategy_prompt += "5. Note any strategic changes, funding events, or leadership transitions\n\n"
        
        strategy_prompt += "## OUTPUT FORMAT:\n"
        strategy_prompt += f"# Precision Intelligence Report: {company_name}\n"
        strategy_prompt += f"Prepared for: Sales meeting with {lead_name}\n"
        strategy_prompt += f"Date: {current_date}\n\n"
        
        strategy_prompt += "## Executive Summary\n"
        strategy_prompt += "[2-3 paragraphs synthesizing the key strategic insights about the company]\n\n"
        
        strategy_prompt += "## Company Profile\n"
        strategy_prompt += "- **Business Model**: [Concise description based on sources]\n"
        strategy_prompt += "- **Target Market**: [Identified market segments/customers]\n"
        strategy_prompt += "- **Unique Value Proposition**: [What differentiates them]\n"
        strategy_prompt += "- **Key Offerings**: [Main products/services]\n\n"
        
        strategy_prompt += "## Strategic Position Analysis\n"
        strategy_prompt += "- **Market Position**: [Where they fit in their competitive landscape]\n"
        strategy_prompt += "- **Growth Trajectory**: [Evidence of expansion/contraction]\n"
        strategy_prompt += "- **Recent Developments**: [New initiatives, pivots, or strategic shifts]\n"
        strategy_prompt += "- **Strengths**: [Based on source material]\n"
        strategy_prompt += "- **Challenges/Vulnerabilities**: [Areas where they might struggle]\n\n"
        
        strategy_prompt += "## Engagement Opportunities\n"
        strategy_prompt += "- **Potential Pain Points**: [Issues they might need help with]\n"
        strategy_prompt += "- **Collaboration Avenues**: [Specific ways our solutions could align]\n"
        strategy_prompt += "- **Conversation Starters**: [3-5 specific talking points based on research]\n\n"
        
        strategy_prompt += "## Sources and Credibility Assessment\n"
        strategy_prompt += "[Brief evaluation of the quality and comprehensiveness of the source material]\n\n"
        
        strategy_prompt += "IMPORTANT: Focus on providing factual, evidence-based insights rather than speculation. Cite specific information from the sources. If you lack sufficient information in any area, acknowledge the limitation rather than making assumptions."
        
        # Call LLM and handle errors
        try:
            logging.info("Calling LLM (gpt-4o) for Third-Party Source Analysis")
            analysis_report = call_llm_text_output(
                prompt=strategy_prompt,
                purpose="Strategic Business Analysis",
                model_name="gpt-4o" 
            )
            
            if analysis_report is not None:
                return analysis_report
            else:
                return "Error: Failed to generate strategic analysis report."
        except Exception as e:
            logging.error(f"Third-party source analysis error: {str(e)}")
            return f"Error: {str(e)}"
            
    def post(self, shared, prep_res, exec_res):
        """Store the analysis in the shared store."""
        shared["precision_intelligence_report"] = exec_res
        
        if isinstance(exec_res, str) and exec_res.startswith("Error:"):
            logging.warning(f"Third-party source analysis failed: {exec_res}")
        else:
            logging.info("Stored precision intelligence report from third-party sources.")
            
        return "default"  # Continue to next node

class GenerateEmail(Node):
    """Calls the utility to generate a personalized email draft."""
    def prep(self, shared):
        """Packages available context for the generation prompt."""
        context = {
            'lead_name': shared.get('lead_name'),
            'company_name': shared.get('company_name'),
            'website_report': shared.get('website_report'),
            'linkedin_report': shared.get('linkedin_report'),
            'precision_intelligence_report': shared.get('precision_intelligence_report')
        }
        logging.info("Preparing context for email generation, including precision intelligence.")
        return context

    def exec(self, context):
        logging.info("Initiating email generation.")
        return ai_generator.generate_email_draft(context)

    def post(self, shared, prep_res, exec_res):
        """Stores the generated subject and body."""
        # exec_res should be a dict {"subject": "...", "body": "..."} even on error (fallback)
        shared["email_subject"] = exec_res.get("subject", "Error: Subject generation failed")
        shared["email_body"] = exec_res.get("body", "Error: Body generation failed")
        logging.info(f"Stored generated email draft (Subject: {shared['email_subject']}).")
        return "default" # Proceed to StoreResults

class StoreResults(Node):
    """Calls the utility to save the final results to the database."""
    def prep(self, shared):
        """Gathers all relevant data from shared store for saving."""
        # Select specific fields to save, ensuring keys match DB columns
        data_to_save = {
            "lead_name": shared.get('lead_name'),
            "last_name": shared.get('last_name'),
            "company_name": shared.get('company_name'),
            "company_website": shared.get('company_website'),
            "linkedin_url": shared.get('linkedin_url'),
            # Store reports only if they are valid dicts and don't represent an error
            "website_analysis_report": shared.get('website_report'),
            "linkedin_analysis_report": shared.get('linkedin_report'),
            "precision_intelligence_report": shared.get('precision_intelligence_report'),
            "generated_email_subject": shared.get('email_subject'),
            "generated_email_body": shared.get('email_body')
            # created_at/updated_at are handled by DB
        }
        logging.info("Preparing final data structure for saving, including precision intelligence report.")
        return data_to_save

    def exec(self, data_to_save):
        logging.info("Initiating save to database.")
        return database.save_to_supabase(data_to_save)

    def post(self, shared, prep_res, exec_res):
        """Logs the success/failure of the save operation."""
        if exec_res:
            logging.info("Successfully saved results to database.")
        else:
            logging.error("Failed to save results to database.")
        return "default" # End of flow