from openai import OpenAI

def call_llm(prompt):    
    client = OpenAI(api_key="YOUR_API_KEY_HERE")
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    if not r.choices or r.choices[0].message is None or r.choices[0].message.content is None:
        raise ValueError("LLM returned empty or filtered response")
    return r.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))