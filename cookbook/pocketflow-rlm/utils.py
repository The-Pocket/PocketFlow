"""LLM adapter kept separate so the cookbook can be tested with a fake model."""

import os


def call_llm(prompt):
    """Call OpenAI's chat API; tests can replace this function with a fake."""

    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""
