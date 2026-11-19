from anthropic import Anthropic
import os

def call_llm(prompt):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key"))
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=20000,
        thinking={"type": "adaptive"},
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    translation = "".join(block.text for block in response.content if block.type == "text")
    if not translation:
        raise ValueError("Claude returned no translation text")
    return translation

if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")