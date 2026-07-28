from anthropic import Anthropic
import os

def call_llm(prompt: str) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-anthropic-api-key")) # Default if key not found
    response = client.messages.create(
        model="claude-3-haiku-20240307", # Using a smaller model for jokes
        max_tokens=150, # Jokes don't need to be very long
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    if not response.content or response.content[0].text is None:

        raise ValueError("LLM returned empty or filtered response")
    return response.content[0].text

if __name__ == "__main__":
    print("Testing Anthropic LLM call for jokes:")
    joke_prompt = "Tell me a one-liner joke about a cat."
    print(f"Prompt: {joke_prompt}")
    try:
        response = call_llm(joke_prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error calling LLM: {e}")
        print("Please ensure your ANTHROPIC_API_KEY environment variable is set correctly.")