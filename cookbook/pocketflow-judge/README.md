# LLM-as-Judge Evaluator-Optimizer

An evaluator-optimizer loop that uses an LLM judge to iteratively improve generated content. A Generator node creates product descriptions while a Judge node scores them for clarity and persuasiveness, sending feedback for revision until the quality threshold is met.

## Features

- Evaluator-optimizer loop pattern with LLM-as-Judge
- Automatic scoring on clarity and persuasiveness (1-10 scale)
- Iterative refinement based on structured feedback
- Configurable pass threshold (score >= 7) with max 3 attempts

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

4. Run with the default product:
    ```bash
    python main.py
    ```

5. Try your own product:
    ```bash
    python main.py --"A smart water bottle that tracks hydration"
    ```

## How It Works

```mermaid
flowchart LR
    gen[Generator] --> judge[Judge]
    judge -->|"fail"| gen
    judge -->|"pass"| done[Done]
```

1. **Generator** writes a product description (incorporating any feedback from previous attempts)
2. **Judge** rates the description 1-10 for clarity and persuasiveness
3. If score >= 7, the description passes and the flow ends
4. If score < 7, the Judge provides specific feedback and loops back to the Generator
5. After 3 attempts, the current draft is accepted regardless of score

## Files

- [`main.py`](./main.py): CLI entry point that sets up and runs the flow
- [`flow.py`](./flow.py): Defines the evaluator-optimizer flow with Generator-Judge loop
- [`nodes.py`](./nodes.py): Generator and Judge node implementations
- [`utils.py`](./utils.py): OpenAI LLM wrapper utility
- [`requirements.txt`](./requirements.txt): Python dependencies

## Example Output

```
🤔 Generating product description for: A noise-cancelling wireless headphone with 30-hour battery life

✍️  --- Draft (Attempt 1) ---
Experience uninterrupted audio bliss with our premium noise-cancelling wireless
headphones. Advanced ANC technology blocks out the world while delivering
crystal-clear sound, and with a marathon 30-hour battery life, your music
never stops.

🔍 Judge Score: 8/10
💡 Reasoning: Clear, concise, and highlights key features effectively.
✅ PASS - Description accepted!

=== Final Result ===
📝 Description: Experience uninterrupted audio bliss with our premium noise-cancelling ...
⭐ Score: 8/10
====================
```
