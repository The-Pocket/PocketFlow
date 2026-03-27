# Adversarial Debate

An adversarial reasoning system where two LLM advocates argue opposing sides of a claim, and an impartial LLM judge evaluates which argument is stronger. This pattern improves decision-making by forcing consideration of multiple perspectives.

## Features

- Two-sided adversarial debate with structured arguments
- Advocate FOR presents evidence-based supporting arguments
- Advocate AGAINST rebuts and presents counterarguments
- Impartial judge scores both sides and picks the winner

## Getting Started

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Set up your OpenAI API key:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```

3. Verify your API key works:
    ```bash
    python utils.py
    ```

4. Run with the default claim:
    ```bash
    python main.py
    ```

5. Try your own claim:
    ```bash
    python main.py --"AI will replace most jobs within 10 years"
    ```

## How It Works

```mermaid
flowchart LR
    for_node[AdvocateFor] --> against_node[AdvocateAgainst] --> judge_node[JudgeDebate]
```

1. **AdvocateFor** receives the claim and builds the strongest possible case in favor
2. **AdvocateAgainst** reads the opposing argument, rebuts its points, and argues against the claim
3. **JudgeDebate** evaluates both arguments for reasoning quality, evidence, and persuasiveness, then picks a winner

## Files

- [`main.py`](./main.py): CLI entry point that sets up and runs the debate flow
- [`flow.py`](./flow.py): Defines the linear debate flow connecting the three nodes
- [`nodes.py`](./nodes.py): AdvocateFor, AdvocateAgainst, and JudgeDebate node implementations
- [`utils.py`](./utils.py): OpenAI LLM wrapper utility
- [`requirements.txt`](./requirements.txt): Python dependencies

## Example Output

```
🤔 Debating claim: "Remote work is more productive than office work"

🟢 --- Advocate FOR ---
Studies from Stanford show remote workers are 13% more productive due to fewer
distractions and a quieter work environment. Employees save an average of 40
minutes daily on commuting, which translates into more focused work time.
💡 Key points:
   - Stanford study shows 13% productivity increase
   - Eliminated commute saves 40+ minutes daily
   - Fewer office distractions improve deep work

🔴 --- Advocate AGAINST ---
While remote work reduces commute time, it often leads to isolation and
communication breakdowns that harm team collaboration. Spontaneous interactions
in offices drive innovation, and many remote workers report blurred work-life
boundaries leading to burnout.
💡 Key points:
   - Communication breakdowns reduce team effectiveness
   - Loss of spontaneous collaboration hurts innovation
   - Blurred boundaries increase burnout risk

⚖️  --- VERDICT ---
🏆 Winner: FOR
📊 Scores - FOR: 7/10 | AGAINST: 6/10
💬 The FOR argument provided stronger empirical evidence with specific studies
   and statistics, while the AGAINST argument relied more on general claims.

=== Debate Summary ===
📋 Claim: "Remote work is more productive than office work"
🏆 Winner: FOR
📊 Scores - FOR: 7/10 | AGAINST: 6/10
⚖️  Verdict: The FOR argument provided stronger empirical evidence...
======================
```
