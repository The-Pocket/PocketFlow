"""Utility function for generating email drafts using AI."""

import json

# Re-using the simulated LLM call from ai_analyzer for simplicity
# In a real app, you might have a dedicated LLM utility or client
# from .ai_analyzer import call_llm # If in the same package

# Temporary simulation if run standalone
def call_llm_gen_temp(prompt: str, purpose: str) -> str:
    print(f"\n--- Simulating LLM Call ({purpose}) ---")
    print(f"Prompt (first 150 chars): {prompt[:150]}...")
    # Simulate a response
    response = json.dumps({
        "subject": "Exploring Synergy for [Company Name]",
        "body": "Hi [Lead Name],\n\nSaw your work on [Recent Focus/Skill] on LinkedIn - impressive!\n\nGiven [Company Name]'s focus on [Website Product/Service], I thought our solution, which helps companies like yours achieve [Value Proposition], might be relevant.\n\nWould you be open to a brief chat next week?\n\nBest,\n[Your Name]"
    })
    print(f"Simulated LLM Response: {response}")
    print("--- End LLM Simulation ---")
    return response

def generate_email_draft(context: dict) -> dict:
    """
    Placeholder for generating a personalized email draft using an LLM.

    Args:
        context: Dictionary containing lead info, analysis reports, etc.
                 Expected keys (examples): 'lead_name', 'company_name', 
                 'website_report' (dict), 'linkedin_report' (dict).

    Returns:
        A dictionary containing the generated email subject and body.
    """
    print("\nGenerating email draft...")

    # Prepare the input for the prompt, handling missing data gracefully
    lead_name = context.get('lead_name', 'there') # Default to 'there'
    company_name = context.get('company_name', '')
    
    # Extract info from reports if they exist
    website_info = "No website data available." 
    if context.get('website_report') and not context['website_report'].get('error'):
        ws_report = context['website_report']
        products = ", ".join(ws_report.get('products_services', []))
        audience = ws_report.get('target_audience', '')
        value_prop = ws_report.get('value_proposition', '')
        website_info = f"Company Products/Services: {products}. Target Audience: {audience}. Value Proposition: {value_prop}."

    linkedin_info = "No LinkedIn data available."
    if context.get('linkedin_report') and not context['linkedin_report'].get('error'):
        li_report = context['linkedin_report']
        career_summary = li_report.get('career_summary', '')
        skills = ", ".join(li_report.get('key_skills', []))
        focus = li_report.get('recent_focus', '')
        linkedin_info = f"Professional Summary: {career_summary}. Key Skills: {skills}. Recent Focus: {focus}."

    # Construct the prompt
    prompt = f"""
    You are an AI assistant generating a personalized cold outreach email.
    Your goal is to write a concise, relevant, and engaging email to a lead.

    **Lead Information:**
    Name: {lead_name}
    Company: {company_name}

    **Research Findings:**
    Website Analysis: {website_info}
    LinkedIn Profile Analysis: {linkedin_info}

    **Instructions:**
    1. Write a short, compelling subject line.
    2. Write a brief email body (3-4 sentences).
    3. Personalize the email using specific details from the research findings (e.g., mention a skill, a company product, or their focus).
    4. Maintain a professional and friendly tone.
    5. End with a clear call to action (e.g., asking for a brief chat).
    6. Output ONLY a JSON object with keys "subject" and "body".

    **JSON Output:**
    """

    # Call the LLM simulation (using temporary one here)
    raw_response = call_llm_gen_temp(prompt, purpose="Email Generation")

    try:
        # Parse the JSON response
        email_result = json.loads(raw_response)
        # Basic validation
        if isinstance(email_result, dict) and 'subject' in email_result and 'body' in email_result:
             # Simple placeholder replacement (can be improved)
             email_result['body'] = email_result['body'].replace("[Lead Name]", lead_name if lead_name != 'there' else 'colleague')
             email_result['body'] = email_result['body'].replace("[Company Name]", company_name)
             # You might add more sophisticated placeholder logic here
             return email_result
        else:
             raise ValueError("Missing subject or body key")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: LLM response was not valid JSON for email generation: {e}")
        # Fallback email
        return {
            "subject": f"Interest in {company_name}",
            "body": f"Hi {lead_name},\n\nI came across your profile and wanted to reach out.\n\nWould you be open to a brief discussion?\n\nBest,\n[Your Name]"
        }

if __name__ == '__main__':
    # Example usage for testing
    test_context = {
        "lead_name": "Jordan Lee",
        "company_name": "Innovate Dynamics",
        "website_report": {
            "analysis_type": "website",
            "products_services": ["AI Chatbots", "Automation Tools"],
            "target_audience": "E-commerce Businesses",
            "value_proposition": "Boost customer engagement 24/7",
            "raw_length": 1200
        },
        "linkedin_report": {
            "analysis_type": "linkedin_profile",
            "career_summary": "Product Manager focused on conversational AI.",
            "key_skills": ["Product Management", "AI", "NLP", "Agile"],
            "recent_focus": "Improving chatbot accuracy",
            "name": "Jordan Lee"
        }
    }
    email_draft = generate_email_draft(test_context)
    print("\n--- Generated Email Draft ---")
    print(f"Subject: {email_draft.get('subject')}")
    print(f"Body:\n{email_draft.get('body')}")
    print("---------------------------")

    # Test with missing data
    test_context_minimal = {
        "lead_name": "Chris",
        "company_name": "Old Tech",
    }
    email_draft_minimal = generate_email_draft(test_context_minimal)
    print("\n--- Generated Email Draft (Minimal Data) ---")
    print(f"Subject: {email_draft_minimal.get('subject')}")
    print(f"Body:\n{email_draft_minimal.get('body')}")
    print("---------------------------") 