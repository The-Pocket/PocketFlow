---
layout: default
title: "Workflow"
parent: "Design Pattern"
nav_order: 2
---

# Workflow

Many real-world tasks are too complex for one LLM call. The solution is to **Task Decomposition**: decompose them into a [chain](../core_abstraction/flow.md) of multiple Nodes.

<div align="center">
  <img src="https://github.com/the-pocket/.github/raw/main/assets/workflow.png?raw=true" width="400"/>
</div>

> - You don't want to make each task **too coarse**, because it may be *too complex for one LLM call*.
> - You don't want to make each task **too granular**, because then *the LLM call doesn't have enough context* and results are *not consistent across nodes*.
> 
> You usually need multiple *iterations* to find the *sweet spot*. If the task has too many *edge cases*, consider using [Agents](./agent.md).
{: .best-practice }

### Example: Article Writing

```python
class GenerateOutline(Node):
    def prep(self, shared): return shared["topic"]
    def exec(self, topic): return call_llm(f"Create a detailed outline for an article about {topic}")
    def post(self, shared, prep_res, exec_res): shared["outline"] = exec_res

class WriteSection(Node):
    def prep(self, shared): return shared["outline"]
    def exec(self, outline): return call_llm(f"Write content based on this outline: {outline}")
    def post(self, shared, prep_res, exec_res): shared["draft"] = exec_res

class ReviewAndRefine(Node):
    def prep(self, shared): return shared["draft"]
    def exec(self, draft): return call_llm(f"Review and improve this draft: {draft}")
    def post(self, shared, prep_res, exec_res): shared["final_article"] = exec_res

# Connect nodes
outline = GenerateOutline()
write = WriteSection()
review = ReviewAndRefine()

outline >> write >> review

# Create and run flow
writing_flow = Flow(start=outline)
shared = {"topic": "AI Safety"}
writing_flow.run(shared)
```

For *dynamic cases*, consider using [Agents](./agent.md).