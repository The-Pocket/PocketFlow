# Run Budget: a dollar ceiling for one flow run

A flow that fans out (here, a parallel batch that summarizes several
documents, then a step that combines them) makes many LLM calls for one
request. This example gives each **flow run** its own dollar budget. Calls
that fit are answered; a call that would push the run over its budget is
refused before it reaches OpenAI, and the flow falls back instead of
crashing.

It uses [Inferrail](https://github.com/domondi1/inferrail), an open-source
gateway that runs inside the process (`inferrail.start()`), reserves each
call's worst-case cost atomically before sending it (so parallel calls
can't all spend the same remaining dollars), and keeps a per-run cost
record without storing prompts or responses.

## Run it

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py            # job 1 gets $0.05; job 2 gets $0.0002 on purpose
```

`MODEL` defaults to an example model id; set it to any model your account
can use (`export MODEL=...`).

Output looks like:

```
=== summary-job-1 (budget $0.05) ===
summarized: 4/4  skipped by budget: []
<combined summary>

=== summary-job-2 (budget $0.0002) ===
summarized: 3/4  skipped by budget: ['support']
Not combined: the run's budget was used up.
```

How many calls fit the tight budget depends on the model and prompt
sizes. Then see what each run cost:

```bash
inferrail work summary-job-1
```

## How it works

- `utils.call_llm` sends every call of a run with the same two headers:
  `X-Inferrail-Attribute-Work-Id` (the run) and `X-Inferrail-Budget-Usd`
  (its budget). The first call creates the budget; nothing is set up
  beforehand.
- A refused call comes back as HTTP 402, raised as `BudgetReached`.
- `exec_fallback_async` turns it into a skipped item, and the nodes use
  `max_retries=1`, since retrying a refused call won't change the answer
  (and is refused again without cost).
- Each call reserves its prompt plus `max_tokens` at the model's price,
  so set `max_tokens`. A model Inferrail has no price for is refused under
  a budget rather than guessed.
