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

# Example usage
if __name__ == "__main__":
    print(call_llm("Tell me a short joke"))
