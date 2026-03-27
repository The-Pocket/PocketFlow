# Lead Generation Pipeline

An automated sales pipeline that scrapes leads, enriches them with company intel, uses an LLM to score fit, and generates personalized cold emails for top prospects.

## Features

- Loads sample lead data (no external scraping APIs needed)
- Enriches leads with simulated company information
- Scores each lead 1-10 using an LLM based on need, seniority, and technical role
- Generates personalized 3-sentence cold emails for high-scoring leads (>= 6)

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Test your API key:
```bash
python utils.py
```

4. Run the pipeline:
```bash
python main.py
```

## How It Works

```mermaid
graph LR
    A[ScrapeLeads] --> B[EnrichLeads]
    B --> C[ScoreLeads]
    C --> D[PersonalizeEmails]
```

1. **ScrapeLeads** — Loads sample lead data (name, title, company)
2. **EnrichLeads** — Adds company intel such as funding stage, tech stack, and team size
3. **ScoreLeads** — LLM rates each lead 1-10 on fit for the product
4. **PersonalizeEmails** — Generates tailored cold emails for every lead scoring 6+

## Files

- [`main.py`](./main.py) — Entry point; runs the pipeline and prints results
- [`flow.py`](./flow.py) — Wires the four nodes into a linear chain
- [`nodes.py`](./nodes.py) — ScrapeLeads, EnrichLeads, ScoreLeads, PersonalizeEmails
- [`utils.py`](./utils.py) — `call_llm` helper, product description, and sample lead data

## Example Output

```
🚀 Starting Lead-Generation Pipeline

📋 Step 1 — Scraping leads
🔍 Step 2 — Enriching leads
🤔 Step 3 — Scoring leads with LLM
✍️  Step 4 — Personalizing emails

  📋 Loaded 3 leads
  🔍 Enriched 3 leads with company intel
  🟢 Priya Patel (Head of AI): 10/10 — Seed-stage AI chatbot company pivoting to LLMs
  🟢 Sarah Chen (CTO): 9/10 — CTO at LLM-powered analytics company using Python
  🟢 Marcus Johnson (VP Engineering): 7/10 — Building AI code assistant on GCP

  ✅ Generated 3 personalized emails

--- Priya Patel (Head of AI @ FinBot) | Score: 10/10 ---
Subject: 100-line LLM framework for FinBot

Priya, I saw FinBot's recent pivot to LLM-based financial advice.
PocketFlow helps teams like yours rapidly prototype AI applications
with zero dependencies. Would you have 15 minutes next week to explore
if PocketFlow could streamline your development?
```
