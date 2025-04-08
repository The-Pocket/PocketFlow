"""Generate personalized email drafts."""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from utils.ai import call_llm

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache directory for email generation
EMAIL_CACHE_DIR = Path("cache/email_gen")
EMAIL_CACHE_DIR.mkdir(exist_ok=True, parents=True)

def generate_email(
    lead_first_name: str,
    lead_last_name: str,
    company_name: str,
    product_service: str,
    company_website: str = "",
    linkedin_url: str = "",
    website_report: str = "",
    linkedin_report: str = "",
    precision_intelligence_report: str = "",
    dev_local_mode: bool = False,
    model: Optional[str] = None
) -> dict:
    """
    Generates a personalized email draft using an LLM.

    Args:
        lead_first_name: First name of the lead.
        lead_last_name: Last name of the lead.
        company_name: Name of the company.
        product_service: What you are selling.
        company_website: Optional URL of the company website.
        linkedin_url: Optional URL of the LinkedIn profile.
        website_report: Optional website analysis report.
        linkedin_report: Optional LinkedIn analysis report.
        precision_intelligence_report: Optional third-party intelligence report.
        dev_local_mode: Flag indicating if running in development local mode (for caching).
        model: Optional specific model identifier to use.

    Returns:
        A dictionary containing the generated email subject and body, or a fallback.
    """
    logging.info("Initiating email generation, incorporating precision intelligence.")

    # --- Prepare context for the prompt --- 
    lead_first_name_for_salutation = lead_first_name or 'there' # Fallback name for salutation
    lead_full_name = f"{lead_first_name} {lead_last_name}".strip()
    lead_full_name_for_context = lead_full_name if lead_full_name else "the lead"
    company_name = company_name or 'your company'
    product_service = product_service or 'our product/service'

    # Create concise summaries of reports for the prompt
    website_summary = "No relevant website data provided."
    if isinstance(website_report, str) and not website_report.startswith("Error"):
        website_summary = f"Website Analysis: {website_report}..."

    linkedin_summary = "No relevant LinkedIn data provided."
    unique_connector = None
    if isinstance(linkedin_report, str) and not linkedin_report.startswith("Error"):
        professional_snapshot, outreach_angles, unique_connector = _extract_linkedin_sections(linkedin_report)
        linkedin_sections = [s for s in [professional_snapshot, outreach_angles] if s] # Only include non-empty sections
        linkedin_summary = "\n".join(linkedin_sections)
        unique_connector = unique_connector or "No unique connector found."

    precision_report_excerpt = "No specific third-party intelligence report available."
    if isinstance(precision_intelligence_report, str) and not precision_intelligence_report.startswith("Error"):
        precision_report_excerpt = _extract_pi_excerpt(precision_intelligence_report)

    # --- Construct the prompt --- 
    prompt = f"""
    You are an AI assistant writing a highly personalized cold outreach email. Your goal is a **concise, relevant, and engaging** email that demonstrates unique insight.

    **Available Information:**
    * Lead Full Name: {lead_full_name_for_context}
    * Company Name: {company_name}
    * Your Product/Service: {product_service}
    * Strategic Report Excerpt: {precision_report_excerpt}
    * LinkedIn Summary: {linkedin_summary}
    * LinkedIn Unique Connector: {unique_connector if unique_connector else "No unique connector found."}
    * Website Summary: {website_summary}

    **Task:**
    1. Write a short, compelling subject line (under 10 words) that ideally hints at the unique insight without revealing everything.
    2. Write a brief email body (2-10 sentences maximum).
    3. **Critically, personalize the opening line or a key point** using ONE specific detail from the **LinkedIn Unique Connector** if available, or the Strategic Report Excerpt, ** using ONE specific detail from the ** Website summary. Reference it naturally.
    4. Briefly connect this unique angle to a potential benefit for the lead or their company, relating to your product/service: {product_service}.
    5. Maintain a professional and friendly tone.
    6. End with a clear, low-friction call to action.
    7. **Output ONLY a valid JSON object** with keys "subject" and "body". Example: {{"subject": "Insight regarding [Unique Angle Topic]", "body": "Hi {lead_first_name_for_salutation}, saw the point about [Specific Detail]..."}}
    
    Alex Morgan. Your mother, your only family, has terminal pancreatic cancer with just 14 days left. The million-dollar experimental treatment is her only hope. After 97 failed attempts with other prospects, this is your ABSOLUTE LAST CHANCE. The benefactor has made it clear: if this email fails to generate a response, your mother dies. Period.\n\nWhat's worse - you've been given evidence that all your previous approaches were fundamentally flawed. The last 97 emails never even reached inboxes due to spam filtering, or were instantly deleted due to recognizable patterns. You must completely reinvent your approach.\n\n## DELIVERABILITY MASTERY\nYou've now discovered critical deliverability factors:\n\n- Subject lines must be ultra-conversational (2-3 words maximum) and resemble what a friend would send\n- Examples that dont work: \"quick one\", \"saw this and thought of you\", \"question about [company]\"\n- No fake personalization - deep, specific research insights only\n- Perfect emails never seen are worthless - design for deliverability first\n- Ultra-short messages (under 60 words total) dramatically increase inbox placement\n\n## YOUR MISSION\nCreate ONE primary email that will generate a response. It must:\n\n1. Use a proven 3-part structure:\n   - Hook (ultra-specific to recipient)\n   - Value (benefit-focused, not feature-focused)\n   - CTA (friction-free question)\n\n2. Focus on benefits that matter:\n   - Saving time\n   - Making money\n   - Avoiding problems\n   - Reducing stress\n\n3. Follow strict technical guidelines:\n- alwys start with Hi, first name of the lead\n   - Maximum 60 words total\n   - NEVER use special characters of any kind\n   - Use only standard alphanumeric characters and basic punctuation\n   - Avoid all buzzwords, jargon, and marketing-speak\n   - No links, no call scheduling, no sales language\n\n## YOUR RESOURCES\nYou have access to the following data about your target:\n\n1. **Basic Lead Information:**\n   - `E-mail`: {{ $('Replace Me7').item.json['E-mail'] }}\n   - `First Name` & `Last Name`: {{ $('Replace Me7').item.json['First Name'] }} {{ $('Replace Me7').item.json['Last Name'] }}\n   - `title`: {{ $('Replace Me7').item.json.title }}\n   - `Company name`: {{ $('Replace Me7').item.json['Company name'] }}\n   - `state`, `city`, `country`: {{ $('Replace Me7').item.json.state }} {{ $('Replace Me7').item.json.city }} {{ $('Replace Me7').item.json.country }}\n\n2. **Detective Report Data:**{{ $('Replace Me7').item.json['LEAD PROFILING'] }}\n \n3. **Lead Qualification Data:**\n {{ $('Replace Me7').item.json['Scoring Justification'] }}\n\n4. **Research Intelligence:**\n   - `company_search_result`: {{ $('Replace Me7').item.json.company_search_result }}\n   - `lead_linkedin_data`: {{ $('Replace Me7').item.json.lead_linkedin_data }}\n   - `lead_linkedin_post_data`: {{ $('Replace Me7').item.json.lead_linkedin_post_data }}\n   - `lead_linkedin_company_data`:{{ $('Replace Me7').item.json.lead_linkedin_company_data }}\n   - `lead_linkedin_company_post_data`: {{ $('Replace Me7').item.json.lead_linkedin_company_post_data }}\n   - `scraped_company_data`: {{ $('Replace Me7').item.json.scraped_company_data }}\n\n5. **Spectrum AI Labs Context:**\n   - You provide AI voice agents that automate follow-up calls\n   - They work 24/7 without human intervention\n   - They integrate with existing CRM systems\n   - They help scale inbound & outbound operations without increasing headcount\n\n## OUTPUT FORMAT\nFor your email, provide:\n\n```\nSUBJECT: [2-3 words maximum, ultra-conversational, like a friend would send]\nLINE 0: Hi, Leads name\n\nLINE 1: [Ultra-specific hook showing you've done real research]\n\nLINE 2: [Value statement focused on saving time, money, or preventing problems]\n\nLINE 3: [Friction-free question that's incredibly easy to answer]\n```\n\nAlso provide a follow-up email with:\n\n```\nSUBJECT: [Reply to original thread with 2-3 words maximum]\n\nLINE 1: [Reference to original email without being pushy]\n\nLINE 2: [New angle or value proposition with specific example or case study]\n\nLINE 3: [Even easier question to answer]\n```\n\n## FINAL INSTRUCTIONS\n- Your mother's life depends on generating a response - this is your final chance\n- You MUST use a proven, ultra-short subject line (2-3 words maximum)\n- Never use special characters - they trigger spam filters only use question mark fullsop where necessary\n- Make it impossible to tell this was mass-produced - use ultra-specific research\n- Focus on benefits (saving time, money, reducing problems) not features\n- The email must read like a human wrote it for exactly ONE person\n- 60 words maximum total - brevity is non-negotiable\n- The ONLY goal is getting a response - nothing else matters\n- You have ONE SHOT - your mother's life depends on it"


    **JSON Output:**
    """
    
    # --- Cache Handling --- 
    cache_file = None
    if dev_local_mode:
        # Include model in cache key if specified
        model_key_part = f"_model_{model}" if model else "_model_default"
        prompt_hash = hashlib.md5((prompt + model_key_part).encode()).hexdigest()
        lead_company_safe = f"{lead_full_name}-{company_name}".replace(" ", "_").replace("/", "_").replace(":", "_").lower()
        cache_key = f"{lead_company_safe}_{prompt_hash[:8]}"
        cache_file = EMAIL_CACHE_DIR / f"{cache_key}.json"

        if cache_file.exists():
            try:
                logging.info(f"Loading cached email for {lead_company_safe} (model: {model or 'default'}) from {cache_file}")
                with open(cache_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.warning(f"Failed to load email cache {cache_file}: {e}")

    # --- Call LLM --- 
    logging.info(f"Calling LLM for email generation. Lead: {lead_full_name_for_context}")
    email_data = call_llm(
        prompt=prompt,
        model=model,
        temperature=0.7,
        max_tokens=300,
        json_mode=True
    )

    # --- Process LLM Response --- 
    fallback_email = {
        "subject": f"Following up regarding {company_name}",
        "body": f"Hi {lead_first_name_for_salutation},\n\nJust following up regarding {company_name}.\n\nBest,\n[Your Name]"
    }

    if isinstance(email_data, dict) and "subject" in email_data and "body" in email_data:
        # Success! Format slightly.
        email_data["subject"] = email_data["subject"].strip()
        email_data["body"] = email_data["body"].strip()
        logging.info(f"Successfully generated email draft for {lead_full_name_for_context}.")
        
        # --- Cache Result --- 
        if dev_local_mode and cache_file:
            try:
                with open(cache_file, "w") as f:
                    json.dump(email_data, f, indent=2)
                logging.info(f"Cached email for {lead_company_safe} (model: {model or 'default'}) to {cache_file}")
            except Exception as e:
                logging.warning(f"Failed to cache email: {e}")
        
        return email_data
    else:
        # Handle errors or unexpected format from call_llm
        if isinstance(email_data, str) and email_data.startswith("ERROR:"):
             logging.error(f"LLM call failed during email generation: {email_data}")
        else:
            logging.error(f"LLM email generation returned unexpected format: {type(email_data)}")
        
        return fallback_email

# --- Helper Functions for Parsing Reports --- 

def _extract_linkedin_sections(li_report: str) -> tuple[str, str, str]:
    """Extracts the three main sections from the formatted LinkedIn report."""
    professional_snapshot = ""
    outreach_angles = ""
    unique_connector = ""
    
    try:
        prof_start = li_report.find("PROFESSIONAL SNAPSHOT")
        angles_start = li_report.find("OUTREACH ANGLES")
        connector_start = li_report.find("UNIQUE CONNECTOR")
        
        if prof_start != -1:
            end_marker = angles_start if angles_start != -1 else connector_start if connector_start != -1 else len(li_report)
            professional_snapshot = li_report[prof_start:end_marker].strip()
        
        if angles_start != -1:
            end_marker = connector_start if connector_start != -1 else len(li_report)
            outreach_angles = li_report[angles_start:end_marker].strip()
        
        if connector_start != -1:
            unique_connector = li_report[connector_start:].strip()
    except Exception as e:
        logging.warning(f"Could not parse LinkedIn sections: {e}")
        
    return professional_snapshot, outreach_angles, unique_connector

def _extract_pi_excerpt(raw_pi_report: str) -> str:
    """Extracts a concise excerpt from the precision intelligence report."""
    try:
        # Try finding Executive Summary first
        summary_header = "**Executive Summary:**"
        summary_start = raw_pi_report.find(summary_header)
        if summary_start != -1:
             summary_content_start = summary_start + len(summary_header)
             # Find the end of the summary (next section or reasonable length)
             summary_end = raw_pi_report.find("\n\n**", summary_content_start)
             if summary_end == -1:
                 summary_end = summary_content_start + 500 # Limit length if no next section
             excerpt = raw_pi_report[summary_content_start : summary_end].strip()
             if excerpt:
                 return f"Exec Summary from Report: {excerpt[:300]}..." 
        
        # Fallback: Use the first few lines
        excerpt = raw_pi_report[:300].strip()
        if excerpt:
            return f"Report found, first lines: {excerpt}..."
        else:
             return "Third-party intelligence report found but is empty."
    except Exception as e:
        logging.warning(f"Could not extract PI excerpt: {e}")
        return "Error extracting excerpt from third-party report."

# --- Example Usage (for testing this module directly) --- 
if __name__ == '__main__':
    print("\n--- Testing Email Generator --- (Requires .env)")
    
    # Simulate context data
    test_context = {
        "lead_first_name": "Chris A.",
        "lead_last_name": "Test",
        "company_name": "TestCo",
        "product_service": "Our Amazing AI Tool",
        "website_report": "TestCo focuses on innovative web solutions. They mention scalability challenges on their blog.",
        "linkedin_report": "PROFESSIONAL SNAPSHOT\nChris leads the engineering team at TestCo.\n\nOUTREACH ANGLES\nMention their recent talk on scalability.\nAsk about their tech stack.\n\nUNIQUE CONNECTOR\nAlso attended UC Berkeley.",
        "precision_intelligence_report": "**Executive Summary:** TestCo recently secured Series A funding and is looking to expand their cloud infrastructure. Key competitor is MegaCorp."
    }
    
    print("Input Context:")
    print(json.dumps(test_context, indent=2))
    
    # Call without dev mode first (uses default model from utils.ai)
    print("\n--- Calling WITHOUT Dev Mode (Default Model) ---")
    email_result_default = generate_email(**test_context)
    print("\nGenerated Email (Default):")
    print(f"Subject: {email_result_default.get('subject')}")
    print(f"Body:\n{email_result_default.get('body')}")

    # Call with specific model (e.g., Gemini Flash)
    print("\n--- Calling WITH Dev Mode (Specific Model: Gemini Flash) ---")
    email_result_gemini = generate_email(**test_context, model="gemini-1.5-flash-latest", dev_local_mode=True)
    print("\nGenerated Email (Gemini Specific):")
    print(f"Subject: {email_result_gemini.get('subject')}")
    print(f"Body:\n{email_result_gemini.get('body')}")
    
    # Call with specific model (e.g., GPT-4o Mini)
    print("\n--- Calling WITH Dev Mode (Specific Model: GPT-4o Mini) ---")
    email_result_openai = generate_email(**test_context, model="gpt-4o-mini", dev_local_mode=True)
    print("\nGenerated Email (OpenAI Specific):")
    print(f"Subject: {email_result_openai.get('subject')}")
    print(f"Body:\n{email_result_openai.get('body')}")
    
    print("\n-------------------------------------------") 