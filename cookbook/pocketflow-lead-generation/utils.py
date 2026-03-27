import os

def call_llm(prompt):
    """Call LLM — auto-detects OpenAI or Gemini based on available API key."""
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        r = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content
    elif os.environ.get("GEMINI_API_KEY"):
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return r.text
    else:
        raise ValueError("Set OPENAI_API_KEY or GEMINI_API_KEY")

PRODUCT = "PocketFlow — a 100-line LLM framework for building AI apps with zero dependencies"

SAMPLE_LEADS = [
    {
        "name": "Sarah Chen",
        "title": "CTO",
        "company": "DataStack AI",
        "enrichment": "DataStack AI raised $12M Series A, building LLM-powered analytics. 45 employees, hiring ML engineers. Uses Python, AWS, Postgres.",
    },
    {
        "name": "Marcus Johnson",
        "title": "VP Engineering",
        "company": "CloudNine Labs",
        "enrichment": "CloudNine Labs, 120 employees, Series B. Building cloud dev tools. Recently launched AI code assistant. Uses TypeScript, GCP.",
    },
    {
        "name": "Priya Patel",
        "title": "Head of AI",
        "company": "FinBot",
        "enrichment": "FinBot, 30 employees, seed stage. AI chatbot for financial advisors. Just pivoted to LLM-based approach. Uses Python, OpenAI API.",
    },
]

if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")
