import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

api_key = os.getenv("OPENAI_API_KEY")
base_url = "https://api.openai.com/v1"
model = "gpt-4o"


def call_llm(message: str):
    print(f"Calling LLM with message: \n{message}")
    client = OpenAI(api_key=api_key, base_url=base_url)
    response: ChatCompletion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": message}]
    )
    if not response.choices or response.choices[0].message is None or response.choices[0].message.content is None:

        raise ValueError("LLM returned empty or filtered response")
    return response.choices[0].message.content


if __name__ == "__main__":
    print(call_llm("Hello, how are you?"))
