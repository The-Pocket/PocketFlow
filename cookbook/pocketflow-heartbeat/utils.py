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

# Simulated email inbox — some cycles have mail, some don't
INBOX = [
    [],
    [{"from": "boss@work.com", "subject": "Q3 report", "body": "Need the Q3 numbers by Friday."}],
    [],
    [{"from": "client@acme.com", "subject": "Invoice #1042", "body": "Invoice seems wrong. Amount should be $4,500 not $5,400."}],
]

check_count = 0

def check_email():
    """Simulate checking an email inbox. Cycles through INBOX entries."""
    global check_count
    emails = INBOX[check_count % len(INBOX)]
    check_count += 1
    return emails

if __name__ == "__main__":
    print("=== Testing call_llm ===")
    prompt = "In a few words, what is the meaning of life?"
    print(f"Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"Response: {response}")

    print("\n=== Testing check_email ===")
    for i in range(5):
        emails = check_email()
        if emails:
            print(f"  Cycle {i+1}: {len(emails)} email(s) - {emails[0]['subject']}")
        else:
            print(f"  Cycle {i+1}: No emails")
