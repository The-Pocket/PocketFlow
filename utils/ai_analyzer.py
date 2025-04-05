"""Utility functions for AI-based analysis of text and data."""

import json
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, OpenAIError

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client
openai_api_key = os.environ.get("OPENAI_API_KEY") # Use correct key name from user
client: OpenAI | None = None
if openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
        logging.info("OpenAI client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")
        client = None
else:
    logging.warning("OPENAI_API_KEY not found in environment variables. AI analysis/generation utilities will not function.")

# Define the model to use
LLM_MODEL = "gpt-4o-mini"

def call_llm_with_json_output(prompt: str, purpose: str) -> dict:
    """Calls the OpenAI API expecting a JSON response."""
    if not client:
        logging.error("OpenAI client not initialized. Cannot call LLM.")
        return {"error": "OpenAI client not initialized"}
    
    logging.info(f"--- Calling OpenAI API ({purpose}) --- Model: {LLM_MODEL}")
    # logging.debug(f"Full Prompt: {prompt}") # Optional: log full prompt if needed
    
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert assistant. Please respond ONLY with a valid JSON object based on the user's request. Do not include any explanatory text before or after the JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, # Request JSON mode
            temperature=0.5, # Adjust temperature for creativity vs determinism
            max_tokens=1000 # Adjust as needed
        )
        
        raw_response_content = response.choices[0].message.content
        logging.info(f"OpenAI API ({purpose}) raw response received (Length: {len(raw_response_content)}). Attempting to parse JSON.")
        
        # Attempt to parse the JSON response from the LLM
        json_response = json.loads(raw_response_content)
        logging.info(f"Successfully parsed JSON response for {purpose}.")
        return json_response
        
    except json.JSONDecodeError as e:
        logging.error(f"OpenAI API ({purpose}) response was not valid JSON: {e}. Raw response: {raw_response_content}")
        return {"error": f"LLM response was not valid JSON: {e}"}
    except RateLimitError as e:
        logging.error(f"OpenAI API ({purpose}) rate limit exceeded: {e}")
        return {"error": f"OpenAI rate limit exceeded: {e}"}
    except APIError as e:
        logging.error(f"OpenAI API ({purpose}) returned an API Error: {e}")
        return {"error": f"OpenAI API Error: {e}"}
    except OpenAIError as e:
         logging.error(f"OpenAI API ({purpose}) request failed: {e}")
         return {"error": f"OpenAI request failed: {e}"}
    except Exception as e:
        logging.error(f"An unexpected error occurred during OpenAI API call ({purpose}): {e}", exc_info=True)
        return {"error": f"Unexpected error during LLM call: {e}"}


def analyze_website_content(website_text: str) -> dict:
    """
    Analyzes website content using the OpenAI LLM (gpt-4o-mini).

    Args:
        website_text: The raw text content scraped from a website.

    Returns:
        A dictionary containing the structured analysis or an error dictionary.
    """
    logging.info("Initiating website content analysis with OpenAI.")
    if not isinstance(website_text, str) or len(website_text) < 20: # Basic check for valid content
        logging.warning("Skipping website analysis due to insufficient content.")
        return {"error": "Insufficient website content provided"}
    
    # Limit input length to avoid excessive token usage
    max_input_length = 15000 # Adjust based on typical content size and token limits
    if len(website_text) > max_input_length:
         logging.warning(f"Website text truncated to {max_input_length} characters for analysis.")
         website_text = website_text[:max_input_length]

    prompt = f"""
    Analyze the following website content and extract key information.
    Provide the output strictly as a JSON object with the following keys:
    - "analysis_type": (string, should be "website")
    - "products_services": (list of strings, key products/services mentioned)
    - "target_audience": (string, inferred target audience)
    - "value_proposition": (string, main value proposition or company mission)
    - "technologies_mentioned": (list of strings, any specific technologies named, optional)
    
    Website Content:
    --- START CONTENT ---
    {website_text}
    --- END CONTENT ---

    Respond ONLY with the JSON object.
    """
    
    analysis_result = call_llm_with_json_output(prompt, purpose="Website Analysis")
    
    # Add raw length for context, useful later maybe
    if not analysis_result.get('error'):
        analysis_result['raw_length'] = len(website_text) 
    return analysis_result

def analyze_linkedin_profile(profile_data: dict) -> dict:
    """
    Analyzes LinkedIn profile data using the OpenAI LLM (gpt-4o-mini).

    Args:
        profile_data: Dictionary containing scraped LinkedIn profile data.

    Returns:
        A dictionary containing the structured analysis or an error dictionary.
    """
    logging.info("Initiating LinkedIn profile analysis with OpenAI.")
    if not isinstance(profile_data, dict) or not profile_data or profile_data.get('error'):
         logging.warning("Skipping LinkedIn analysis due to invalid or missing profile data.")
         return {"error": "Invalid or missing LinkedIn profile data"}

    # Convert dict to string for the prompt
    try:
         profile_text = json.dumps(profile_data, indent=2)
    except TypeError:
         logging.warning("Could not serialize profile data to JSON for LLM prompt.")
         return {"error": "Could not serialize profile data for LLM prompt"}

    # Limit input length
    max_input_length = 15000
    if len(profile_text) > max_input_length:
         logging.warning(f"LinkedIn profile text truncated to {max_input_length} characters for analysis.")
         profile_text = profile_text[:max_input_length]

    prompt = f"""
    Analyze the following LinkedIn profile data (in JSON format) and extract key professional insights.
    Provide the output strictly as a JSON object with the following keys:
    - "analysis_type": (string, should be "linkedin_profile")
    - "name": (string, the full name from the profile data if available)
    - "headline": (string, the professional headline)
    - "career_summary": (string summarizing trajectory, key roles, focus areas)
    - "key_skills": (list of top 5-7 technical or business skills mentioned)
    - "recent_focus": (string describing current role/interests if apparent from headline/summary/recent experience)
    
    LinkedIn Profile Data:
    --- START DATA ---
    {profile_text}
    --- END DATA ---

    Respond ONLY with the JSON object.
    """

    analysis_result = call_llm_with_json_output(prompt, purpose="LinkedIn Analysis")
    return analysis_result

if __name__ == '__main__':
    # Example usage for testing - Requires .env file with OPENAI_API_KEY
    print("\n=== Testing AI Analyzer (OpenAI) === (Requires .env)")
    
    if not client:
        print("Skipping test: OpenAI client not initialized.")
    else:
        # Test Website Analysis
        print("\n--- Testing Website Analysis ---")
        test_website_content = """
        QuantumLeap Solutions provides bespoke AI algorithms for the financial sector.
        Our flagship product, FinSight Quantum, helps investment banks optimize high-frequency trading risk management using quantum-inspired techniques.
        We target hedge funds and large financial institutions seeking a significant competitive edge through predictive analytics.
        Our core technology is built on Python, JAX, and proprietary quantum simulation libraries.
        """
        website_analysis = analyze_website_content(test_website_content)
        print("\nFinal Website Analysis Output:")
        print(json.dumps(website_analysis, indent=2))

        # Test LinkedIn Analysis
        print("\n\n--- Testing LinkedIn Analysis ---")
        test_profile_data = {
            "profileUrl": "https://linkedin.com/in/sam-rivera-example",
            "fullName": "Sam Rivera",
            "headline": "Lead Quantum AI Engineer @ QuantumLeap Solutions | Ex-FinTech Innovations",
            "summary": "Leading quantum algorithm development for financial modeling. Building predictive engines for market trends. Expert in Python, JAX, ML, and quantum computing applications.",
            "experience": [
                 {"title": "Lead Quantum AI Engineer", "companyName": "QuantumLeap Solutions"},
                 {"title": "Senior Data Scientist", "companyName": "FinTech Innovations"}
            ],
            "skills": ["Quantum Computing", "Machine Learning", "Python", "JAX", "High-Frequency Trading", "Risk Management", "Financial Modeling"]
        }
        linkedin_analysis = analyze_linkedin_profile(test_profile_data)
        print("\nFinal LinkedIn Analysis Output:")
        print(json.dumps(linkedin_analysis, indent=2)) 