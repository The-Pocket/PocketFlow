"""Utility function for generating email drafts using AI."""

import json
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, OpenAIError

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client (can potentially share client if modules are structured differently)
openai_api_key = os.environ.get("OPENAI_API_KEY") 
client: OpenAI | None = None
if openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
        logging.info("OpenAI client initialized successfully for generator.")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client for generator: {e}")
        client = None
else:
    logging.warning("OPENAI_API_KEY not found. AI generation utility will not function.")

# Define the model to use
LLM_MODEL = "gpt-4o-mini"


def generate_email_draft(context: dict) -> dict:
    """
    Generates a personalized email draft using the OpenAI LLM (gpt-4o-mini).

    Args:
        context: Dictionary containing lead info and analysis reports.
                 Includes 'lead_name', 'company_name', 'website_report', 
                 'linkedin_report', 'precision_intelligence_report'.

    Returns:
        A dictionary containing the generated email subject and body, or a fallback.
    """
    if not client:
        logging.error("OpenAI client not initialized for generator. Returning fallback email.")
        return {
            "subject": f"Following up",
            "body": f"Hi {context.get('lead_name', 'there')},\n\nJust following up.\n\nBest,\n[Your Name]"
        }

    logging.info("Initiating email generation with OpenAI, incorporating precision intelligence.")

    # Prepare the input for the prompt, handling missing data gracefully
    lead_name = context.get('lead_name', 'there')
    company_name = context.get('company_name', '')
    
    # Create concise summaries of reports for the prompt
    website_summary = "No relevant website data provided."
    if context.get('website_report') and isinstance(context['website_report'], dict) and not context['website_report'].get('error'):
        ws_report = context['website_report']
        products = ", ".join(ws_report.get('products_services', [])[:2]) # Limit products
        value_prop = ws_report.get('value_proposition', '')
        website_summary = f"Company Info: Sells [{products}], Value Prop: [{value_prop}]"

    linkedin_summary = "No relevant LinkedIn data provided."
    if context.get('linkedin_report') and isinstance(context['linkedin_report'], dict) and not context['linkedin_report'].get('error'):
        li_report = context['linkedin_report']
        headline = li_report.get('headline', '')
        skills = ", ".join(li_report.get('key_skills', [])[:3]) # Limit skills
        focus = li_report.get('recent_focus', '')
        linkedin_summary = f"Role: [{headline}], Skills: [{skills}], Recent Focus: [{focus}]"

    # Precision Intelligence Summary (NEW)
    precision_angle = "No specific third-party angle found."
    precision_context = "No specific third-party context found."
    if context.get('precision_intelligence_report') and isinstance(context['precision_intelligence_report'], dict) and not context['precision_intelligence_report'].get('error'):
        pi_report = context['precision_intelligence_report']
        # Extract the unique angle and potentially a sentiment/context point
        unique_angle_data = pi_report.get('unique_conversation_angle', {})
        if unique_angle_data and unique_angle_data.get('point'):
            precision_angle = unique_angle_data.get('point')
        
        # Try to get a sentiment point as context
        sentiment_data = pi_report.get('customer_sentiment', [])
        if sentiment_data and isinstance(sentiment_data, list) and len(sentiment_data) > 0 and sentiment_data[0].get('point'):
            precision_context = f"Customer sentiment insight: '{sentiment_data[0].get('point')}'"
        # Fallback to industry context if no sentiment
        elif not sentiment_data or not sentiment_data[0].get('point'):
             industry_data = pi_report.get('industry_context', [])
             if industry_data and isinstance(industry_data, list) and len(industry_data) > 0 and industry_data[0].get('point'):
                 precision_context = f"Industry context: '{industry_data[0].get('point')}'"

    # Construct the prompt
    prompt = f"""
    You are an AI assistant writing a highly personalized cold outreach email. Your goal is a **concise, relevant, and engaging** email that demonstrates unique insight.

    **Available Information:**
    * Lead Name: {lead_name}
    * Company Name: {company_name}
    * Unique Third-Party Insight (Angle): {precision_angle}
    * Supporting Third-Party Context: {precision_context}
    * LinkedIn Summary (Optional): {linkedin_summary}
    * Website Summary (Optional): {website_summary}

    **Task:**
    1. Write a short, compelling subject line (under 10 words) that ideally hints at the unique insight without revealing everything.
    2. Write a brief email body (2-4 sentences maximum).
    3. **Critically, use the 'Unique Third-Party Insight (Angle)' as the primary hook** for your opening sentence or a key point. Reference it specifically but naturally (e.g., "Saw the discussion on [Forum] about..." or "Noticed the insight from the [Source] report regarding...").
    4. Briefly connect this unique angle to a potential benefit for the lead or their company, relating to your (unspecified) product/service.
    5. If the unique angle is weak ("No specific third-party angle found."), fall back to using a detail from the LinkedIn or Website summary for personalization.
    6. Maintain a professional and friendly tone.
    7. End with a clear, low-friction call to action.
    8. **Output ONLY a valid JSON object** with keys "subject" and "body". Example: {{"subject": "Insight regarding [Unique Angle Topic]", "body": "Hi {lead_name}, saw the point about [Specific Detail]..."}}
    
    **JSON Output:**
    """

    logging.info(f"Calling OpenAI for email generation. Lead: {lead_name}")
    # Use the generic JSON call function (or adapt if needed)
    try:
         # Re-use the JSON call helper from ai_analyzer (assuming it's importable or defined here)
         # from .ai_analyzer import call_llm_with_json_output
         # For now, duplicating the core call logic here for simplicity
         response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert assistant. Respond ONLY with the valid JSON object requested by the user."}, 
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.7, # Slightly higher temp for generation
            max_tokens=300 
        )
         raw_response_content = response.choices[0].message.content
         logging.info(f"OpenAI API (Email Gen) raw response received (Length: {len(raw_response_content)}). Parsing JSON.")
         email_result = json.loads(raw_response_content)
         
         # Basic validation
         if isinstance(email_result, dict) and 'subject' in email_result and 'body' in email_result:
             logging.info(f"Successfully generated email draft for {lead_name}.")
             # Simple placeholder replacement (can be improved)
             email_result['body'] = email_result['body'].replace("{lead_name}", lead_name if lead_name != 'there' else 'colleague')
             email_result['subject'] = email_result['subject'].replace("{company_name}", company_name)
             email_result['body'] = email_result['body'].replace("{company_name}", company_name)
             # Add more sophisticated placeholder logic here if needed
             return email_result
         else:
             raise ValueError("LLM JSON response missing subject or body key")
             
    except json.JSONDecodeError as e:
        logging.error(f"OpenAI API (Email Gen) response was not valid JSON: {e}. Raw response: {raw_response_content}")
        error_msg = f"LLM response was not valid JSON: {e}"
    except RateLimitError as e:
        logging.error(f"OpenAI API (Email Gen) rate limit exceeded: {e}")
        error_msg = f"OpenAI rate limit exceeded: {e}"
    except APIError as e:
        logging.error(f"OpenAI API (Email Gen) returned an API Error: {e}")
        error_msg = f"OpenAI API Error: {e}"
    except OpenAIError as e:
         logging.error(f"OpenAI API (Email Gen) request failed: {e}")
         error_msg = f"OpenAI request failed: {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during OpenAI API call (Email Gen): {e}", exc_info=True)
        error_msg = f"Unexpected error during email generation: {e}"
    
    # Fallback email if any error occurred
    logging.warning(f"Returning fallback email for {lead_name} due to error: {error_msg}")
    return {
        "subject": f"Quick question regarding {company_name if company_name else 'your work'}",
        "body": f"Hi {lead_name if lead_name != 'there' else 'colleague'},\n\nI came across your profile/company and wanted to reach out.\n\nCould we schedule a brief call next week to discuss potential synergies?\n\nBest regards,\n[Your Name]"
        # Include error message in body? Maybe not user-facing.
        # "body": f"... Error: {error_msg}"
    }


if __name__ == '__main__':
    # Example usage for testing - Requires .env file with OPENAI_API_KEY
    print("\n=== Testing AI Generator (OpenAI) === (Requires .env)")

    if not client:
        print("Skipping test: OpenAI client not initialized.")
    else:
        # Test with good context
        print("\n--- Testing Email Generation (Good Context + Precision) ---")
        test_context_with_pi = {
            "lead_name": "Dr. Evelyn Reed",
            "company_name": "Quantum Dynamics Inc.",
            "website_report": {
                "analysis_type": "website",
                "products_services": ["Quantum Computing Platform", "Algorithm Design"],
                "target_audience": "Research Labs & Pharma",
                "value_proposition": "Accelerate drug discovery with quantum simulations",
                "raw_length": 1200
            },
            "linkedin_report": {
                "analysis_type": "linkedin_profile",
                "name": "Dr. Evelyn Reed",
                "headline": "Chief Scientist at Quantum Dynamics Inc. | Quantum Algorithms Expert",
                "career_summary": "Leading research in quantum algorithms for molecular simulation.",
                "key_skills": ["Quantum Computing", "Python", "Qiskit", "Drug Discovery", "Computational Chemistry"],
                "recent_focus": "Developing novel quantum simulations for protein folding"
            },
            "precision_intelligence_report": {
                "industry_context": [
                    {"point": "Competitor [X] recently launched a similar simulation platform.", "source": "https://news.example/competitor-launch"}
                ],
                "customer_sentiment": [
                    {"point": "Users on G2 praise the platform's ease of use but wish for better visualization tools.", "source": "https://g2.com/quantum-dynamics/reviews"}
                ],
                "unique_conversation_angle": {"point": "Mentioned Quantum Dynamics' focus on protein folding simulations in a recent industry forum post.", "source": "https://forum.example/quantum-post"}
            }
        }
        email_draft = generate_email_draft(test_context_with_pi)
        print(f"\nSubject: {email_draft.get('subject')}")
        print(f"Body:\n{email_draft.get('body')}")
        print("---------------------------")

        # Test with minimal context
        print("\n\n--- Testing Email Generation (Minimal Context) ---")
        test_context_minimal = {
            "lead_name": "Sam Jones",
            "company_name": "General Tech LLC",
            "website_report": {"error": "Scraping failed"}, # Simulate error
            "linkedin_report": None, # Simulate missing data
            "precision_intelligence_report": None # Simulate missing PI report
        }
        email_draft_minimal = generate_email_draft(test_context_minimal)
        print(f"\nSubject: {email_draft_minimal.get('subject')}")
        print(f"Body:\n{email_draft_minimal.get('body')}")
        print("---------------------------") 