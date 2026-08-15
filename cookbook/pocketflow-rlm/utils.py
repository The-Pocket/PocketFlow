"""LLM adapter kept separate so the RLM can be tested with a fake model."""

import os


def call_llm(prompt):
    """Call an OpenAI-compatible chat model for one root or child request."""

    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""
