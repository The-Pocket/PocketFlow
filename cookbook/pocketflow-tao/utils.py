# utils.py

from openai import OpenAI
import os

def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "Your Key Here"),base_url=os.environ.get("OPENAI_API_BASE", "Your API Base Here"))
    r = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "openai/gpt-4.1-nano"),
        messages=[{"role": "user", "content": prompt}]
    )
    if not r.choices or r.choices[0].message is None or r.choices[0].message.content is None:
        raise ValueError("LLM returned empty or filtered response")
    return r.choices[0].message.content

if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")