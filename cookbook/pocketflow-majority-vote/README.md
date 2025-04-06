# Majority Vote Reasoning

This project demonstrates a majority vote implementation that enables LLMs to solve complex reasoning problems by aggregating multiple independent attempts. It's designed to improve problem-solving accuracy through consensus-based reasoning.

## Features

- Improves model reliability on complex problems through multiple attempts
- Works with models like Claude 3.7 Sonnet
- Solves problems that single attempts often fail on
- Provides detailed reasoning traces for verification
- Uses a consensus approach to reduce the impact of occasional reasoning errors

## Getting Started

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Run a test problem to see majority voting in action:
```bash
python main.py
```

4. Try your own reasoning problem:
```bash
python main.py --problem "Your complex reasoning problem here" --tries 5
```

## How It Works

The implementation uses a MajorityVoteNode that processes multiple attempts and finds consensus:

```mermaid
flowchart LR
    mv[MajorityVoteNode] 
```

The MajorityVoteNode:
1. Makes multiple independent attempts to solve the same problem
2. Collects structured answers from each attempt
3. Determines the most frequent answer as the final solution
4. Returns the consensus answer

This approach helps overcome occasional reasoning errors that might occur in individual attempts.

## Example Problem

Example Problem from [Quant Interview](https://www.youtube.com/watch?v=SCP7JptxPU0):

```
You work at a shoe factory. In front of you, there are three pairs of shoes (six individual shoes) with the following sizes: two size 4s, two size 5s, and two size 6s. The factory defines an "acceptable pair" as two shoes that differ in size by a maximum of one size (e.g., a size 5 and a size 6 would be an acceptable pair). If you close your eyes and randomly pick three pairs of shoes without replacement, what is the probability that you end up drawing three acceptable pairs?
```

Below is an example of how the majority vote approach uses Claude 3.7 Sonnet to solve this complex problem:

```
========================
All structured answers: ['0.333', '0.333', '0.333', '0.6', '0.333']
Majority vote => 0.333
Frequency => 4
========================

=== Final Answer ===
0.333
====================
```

This shows that 4 out of 5 attempts yielded the same answer (0.333), which is chosen as the final solution.

## Files

- [`main.py`](./main.py): Implementation of the majority vote node and flow
- [`utils.py`](./utils.py): Simple wrapper for calling the Anthropic model