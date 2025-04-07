"""
Utility functions for working with AI/LLM services.
Prioritizes clients in order: Groq > Gemini > OpenAI
"""

import os
import logging
import json
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv

# Import client libraries
from openai import OpenAI, RateLimitError, APIError, OpenAIError
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from groq import Groq, GroqError

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Client Initialization ---
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_client: Optional[OpenAI] = None

gemini_api_key = os.environ.get("GEMINI_API_KEY")
gemini_client_initialized = False

groq_api_key = os.environ.get("GROQ_API_KEY")
groq_client: Optional[Groq] = None

# Attempt to initialize clients based on priority
priority_client = None # Tracks the highest priority client initialized

if groq_api_key:
    try:
        groq_client = Groq(api_key=groq_api_key)
        # Optional: Add a simple test call like listing models if needed
        # groq_client.models.list()
        priority_client = "groq"
        logging.info("Groq client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Groq client: {e}")
        groq_client = None

if not priority_client and gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_client_initialized = True
        priority_client = "gemini"
        logging.info("Google Gemini client configured successfully.")
    except Exception as e:
        logging.error(f"Failed to configure Google Gemini client: {e}")
        gemini_client_initialized = False

if not priority_client and openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        priority_client = "openai"
        logging.info("OpenAI client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")
        openai_client = None

if not priority_client:
     logging.warning("No LLM client could be initialized (Checked Groq, Gemini, OpenAI). LLM functions will not work.")

# --- Default Models --- 
# Define defaults for each provider
DEFAULT_GROQ_MODEL = "llama3-8b-8192"  # Fast Llama3 model on Groq
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

# --- Core LLM Call Function --- 
def call_llm(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    json_mode: bool = False
) -> Union[str, dict, None]:
    """
    Call the highest priority configured LLM API.

    Args:
        prompt: The prompt text to send to the LLM.
        model: The specific model identifier (e.g., "llama3-8b-8192", "gemini-1.5-flash-latest", "gpt-4o").
               If None, uses the default for the highest priority active provider.
        temperature: Controls randomness (0-1, lower is more deterministic).
        max_tokens: Maximum output tokens (supported by OpenAI & Groq).
        json_mode: If True, instructs the model to output JSON and attempts parsing.

    Returns:
        If json_mode is False: The text response from the LLM as a string.
        If json_mode is True: The parsed JSON response as a dictionary.
        Returns None if no client is available or an error occurs during JSON parsing.
        Returns an error string if an API call fails.
    """

    # --- Determine Provider and Model --- 
    selected_model: str
    provider_to_use: Optional[str] = None

    if model: # If a model is explicitly passed, try to use it
        selected_model = model
        # Basic inference of provider based on model name
        if ("llama" in model or "mixtral" in model) and groq_client:
            provider_to_use = "groq"
        elif "gemini" in model and gemini_client_initialized:
            provider_to_use = "gemini"
        elif "gpt" in model and openai_client:
            provider_to_use = "openai"
        else:
            # If model doesn't match known patterns, use the priority client if available
            if priority_client:
                 provider_to_use = priority_client
                 logging.warning(f"Model '{model}' pattern not recognized, using priority client: {priority_client}")
            else:
                 logging.error(f"Model '{model}' requested, but no client is available or pattern not recognized.")
                 return f"ERROR: No client available for model {model}"
    else: # No model specified, use the default for the priority client
        provider_to_use = priority_client
        if provider_to_use == "groq":
            selected_model = DEFAULT_GROQ_MODEL
        elif provider_to_use == "gemini":
            selected_model = DEFAULT_GEMINI_MODEL
        elif provider_to_use == "openai":
            selected_model = DEFAULT_OPENAI_MODEL
        else:
            error_msg = "No LLM client available (Groq, Gemini, or OpenAI)."
            logging.error(error_msg)
            return f"ERROR: {error_msg}"

    # --- Log the call --- 
    logging.info(f"Calling {provider_to_use.capitalize()} (Model: {selected_model}, Temp: {temperature}, JSON: {json_mode}) Prompt: {len(prompt)} chars")

    # --- Prepare instruction for JSON mode --- 
    json_instruction = "\n\nIMPORTANT: Respond ONLY with a valid JSON object matching the structure requested. Do not include any explanatory text, markdown formatting (like ```json), or anything before or after the JSON object." 
    final_prompt = f"{prompt}{json_instruction if json_mode else ''}"

    try:
        # --- Groq Call --- 
        if provider_to_use == "groq" and groq_client:
            messages = [
                # Groq often works better without a strict system prompt for JSON when using json_mode
                {"role": "user", "content": prompt} 
            ]
            request_params: Dict[str, Any] = {
                "model": selected_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            if json_mode:
                request_params["response_format"] = {"type": "json_object"}

            chat_completion = groq_client.chat.completions.create(**request_params)
            raw_response_content = chat_completion.choices[0].message.content
            
        # --- Gemini Call --- 
        elif provider_to_use == "gemini":
            gen_model = genai.GenerativeModel(
                selected_model,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json" if json_mode else "text/plain",
                    temperature=temperature
                    # max_output_tokens can be added here if needed
                )
            )
            response = gen_model.generate_content(final_prompt) # Use prompt with JSON instruction here for Gemini
            raw_response_content = response.text

        # --- OpenAI Call --- 
        elif provider_to_use == "openai" and openai_client:
            messages = [
                 {"role": "system", "content": "You are an expert assistant." + (json_instruction if json_mode else "")},
                 {"role": "user", "content": prompt}
            ]
            request_params = {
                "model": selected_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            if json_mode:
                request_params["response_format"] = {"type": "json_object"}

            response = openai_client.chat.completions.create(**request_params)
            raw_response_content = response.choices[0].message.content
        else:
            # Should be unreachable
            return "ERROR: Client selection failed unexpectedly."

        # --- Process Response --- 
        logging.info(f"Received {provider_to_use.capitalize()} response ({len(raw_response_content)} chars)")
        
        if json_mode:
            try:
                # Attempt to parse the JSON, removing potential markdown fences
                if raw_response_content.strip().startswith("```json"):
                     json_str = raw_response_content.strip().split("```json", 1)[1].rsplit("```", 1)[0]
                elif raw_response_content.strip().startswith("```"):
                     json_str = raw_response_content.strip().split("```", 1)[1].rsplit("```", 1)[0]
                else:
                     json_str = raw_response_content
                     
                parsed_json = json.loads(json_str)
                if isinstance(parsed_json, dict):
                    return parsed_json
                else:
                    logging.error(f"{provider_to_use.capitalize()} returned valid JSON, but not a dictionary: {type(parsed_json)}")
                    return None
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error ({provider_to_use.capitalize()}): {e}. Raw: {raw_response_content[:100]}...")
                return None
        else:
            return raw_response_content.strip()

    # --- Error Handling --- 
    except GroqError as e: # Groq specific
         error_msg = f"Groq API error: {str(e)}"
         logging.error(error_msg)
         return f"ERROR: {error_msg}"
    except (RateLimitError, APIError, OpenAIError) as e: # OpenAI specific
        error_msg = f"OpenAI API error: {str(e)}"
        logging.error(error_msg)
        return f"ERROR: {error_msg}"
    except GoogleAPIError as e: # Google specific
        error_msg = f"Google API error: {str(e)}"
        logging.error(error_msg)
        return f"ERROR: {error_msg}"
    except Exception as e: # General errors
        error_msg = f"Unexpected error during LLM call ({provider_to_use.capitalize()}): {str(e)}"
        logging.error(error_msg, exc_info=True)
        return f"ERROR: {error_msg}"

# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    print("\n--- Testing LLM Call --- (Requires .env with GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY)")

    active_client = priority_client if priority_client else "None"
    print(f"Highest Priority Active Client: {active_client.capitalize()}")

    if active_client == "None":
        print("Skipping tests: No LLM client initialized.")
    else:
        # Test Text Mode (using default model for the active client)
        test_prompt_text = "Write a one-sentence summary of what PocketFlow is."
        print(f"\nTest Prompt (Text, Default Model - {active_client.capitalize()}): {test_prompt_text}")
        response_text = call_llm(test_prompt_text, temperature=0.7)
        print("\nLLM Response (Text):")
        print(response_text)

        # Test JSON Mode (using default model for the active client)
        test_prompt_json = """
        Analyze the sentiment of this text: 'PocketFlow is amazing!'
        Return your analysis ONLY as a valid JSON object with keys "sentiment" (e.g., "positive", "negative", "neutral") and "confidence" (a float between 0 and 1).
        """
        print(f"\nTest Prompt (JSON, Default Model - {active_client.capitalize()}): {test_prompt_json}")
        response_json = call_llm(test_prompt_json, temperature=0.2, json_mode=True)
        print("\nLLM Response (JSON):")
        if isinstance(response_json, dict):
            print(json.dumps(response_json, indent=2))
        else:
            print(f"Failed to get valid JSON response. Received: {response_json}")

        # --- Test Specific Models --- 
        # Test Groq model (if available)
        if groq_client:
             print(f"\n--- Testing Explicit Groq Model ({DEFAULT_GROQ_MODEL}) ---")
             response_groq = call_llm(test_prompt_text, model=DEFAULT_GROQ_MODEL)
             print("\nLLM Response (Groq Specific):")
             print(response_groq)
             
        # Test Gemini model (if available)
        if gemini_client_initialized:
             print(f"\n--- Testing Explicit Gemini Model ({DEFAULT_GEMINI_MODEL}) ---")
             response_gemini = call_llm(test_prompt_text, model=DEFAULT_GEMINI_MODEL)
             print("\nLLM Response (Gemini Specific):")
             print(response_gemini)
             
        # Test OpenAI model (if available)
        if openai_client:
             print(f"\n--- Testing Explicit OpenAI Model ({DEFAULT_OPENAI_MODEL}) ---")
             response_openai = call_llm(test_prompt_text, model=DEFAULT_OPENAI_MODEL)
             print("\nLLM Response (OpenAI Specific):")
             print(response_openai)

        print("\n-------------------------------------------") 