import os

import inferrail
from openai import APIStatusError, AsyncOpenAI

# Inferrail runs inside this process and enforces a dollar budget per run.
# The provider key is read from OPENAI_API_KEY.
BASE_URL = inferrail.start()

# An example model id: use any model your OpenAI account can use.
MODEL = os.environ.get("MODEL", "gpt-4o-mini")


class BudgetReached(Exception):
    """The run's budget can't cover this call; it was not sent to OpenAI."""


async def call_llm(prompt: str, run_id: str, budget_usd: str) -> str:
    client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key="unused",  # the provider key stays with Inferrail
        default_headers={
            "X-Inferrail-Attribute-Work-Id": run_id,  # every call of this run
            "X-Inferrail-Budget-Usd": budget_usd,  # created on the run's first call
        },
    )
    try:
        r = await client.chat.completions.create(
            model=MODEL,
            max_tokens=150,  # each call reserves its worst case before it is sent
            messages=[{"role": "user", "content": prompt}],
        )
    except APIStatusError as e:
        if e.status_code == 402:
            raise BudgetReached(str(e)) from e
        raise
    return r.choices[0].message.content
