<div align="center">
  <img src="./assets/title.png" width="600"/>
</div>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
<a href="https://discord.gg/hUHHE9Sa6T">
<img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow is a [100-line](pocketflow/__init__.py) minimalist LLM framework

- **Lightweight**: Just 100 lines. Zero bloat, zero dependencies, zero vendor lock-in.
- **Expressive**: Everything you love—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), and more.

- **[Agentic Coding](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Let AI Agents (e.g., Cursor AI) build Agents—10x productivity boost!

- To install, `pip install pocketflow`or just copy the [source code](pocketflow/__init__.py) (only 100 lines).
- To learn more, check out the [documentation](https://the-pocket.github.io/PocketFlow/). For an in-depth design dive, read the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md).
- 🎉 We now have a [discord](https://discord.gg/hUHHE9Sa6T)!

## Why Pocket Flow?

Current LLM frameworks are bloated... You only need 100 lines for LLM Framework!

<div align="center">
  <img src="./assets/meme.jpg" width="400"/>

|                | **Abstraction** |                     **App-Specific Wrappers**                      |                       **Vendor-Specific Wrappers**                       |                **Lines**                 |                  **Size**                   |
| -------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain      |  Agent, Chain   |      Many <br><sup><sub>(e.g., QA, Summarization)</sub></sup>      |      Many <br><sup><sub>(e.g., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI         |  Agent, Chain   | Many <br><sup><sub>(e.g., FileReadTool, SerperDevTool)</sub></sup> | Many <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent      |      Agent      |   Some <br><sup><sub>(e.g., CodeAgent, VisitWebTool)</sub></sup>   |  Some <br><sup><sub>(e.g., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph      |  Agent, Graph   |       Some <br><sup><sub>(e.g., Semantic Search)</sub></sup>       | Some <br><sup><sub>(e.g., PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen        |      Agent      |   Some <br><sup><sub>(e.g., Tool Agent, Chat Agent)</sub></sup>    | Many <sup><sub>[Optional]<br> (e.g., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(core-only)</sub></sup> | +26MB <br><sup><sub>(core-only)</sub></sup> |
| **PocketFlow** |    **Graph**    |                              **None**                              |                                 **None**                                 |                 **100**                  |                  **+56KB**                  |

</div>

## How does Pocket Flow work?

The [100 lines](pocketflow/__init__.py) capture the core abstraction of LLM frameworks: Graph!
<br>

<div align="center">
  <img src="./assets/abstraction.png" width="900"/>
</div>
<br>

From there, it's easy to implement popular design patterns like ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.
<br>

<div align="center">
  <img src="./assets/design.png" width="900"/>
</div>
<br>
✨ Below are basic tutorials:

<div align="center">
  
|  Name  | Difficulty    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Dummy*   | A basic chat bot with conversation history |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Dummy*   | A simple Retrieval-augmented Generation process |
| [Workflow](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Dummy*   | A writing workflow that outlines, writes content, and applies styling |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *Dummy* | A resume qualification processor using map-reduce pattern for batch evaluation |
| [Agent](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Dummy*   | A research agent that can search the web and answer questions |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Dummy*   | A real-time LLM streaming demo with user interrupt capability |
| [Multi-Agent](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Beginner* | A Taboo word game for asynchronous communication between two agents |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Beginner* | Research agent is getting unreliable... Let's build a supervision process|
| [Parallel](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Beginner*   | A parallel execution demo that shows 3x speedup |
| [Thinking](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Beginner*   | Solve complex reasoning problems through Chain-of-Thought |
| [Memory](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Beginner* | A chat bot with short-term and long-term memory |

</div>

👀 Want to see other tutorials for dummies? [Create an issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## How to Use Pocket Flow?

🚀 Through **Agentic Coding**—the fastest LLM App development paradigm-where _humans design_ and _agents code_!

<br>
<div align="center">
  <a href="https://youtu.be/Cf38Bi8U0Js" target="_blank">
    <img src="./assets/tutorial.png" width="500" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Below are examples of more complex LLM Apps:

<div align="center">
  
|  App Name     |  Difficulty    | Topics  | Human Design | Agent Code |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Build Cursor with Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>We'll reach the singularity soon ...</sup></sub> | ★★★ <br> *Advanced*   | [Agent](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Design Doc](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Flow Code](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Ask AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Ask AI Paul Graham, in case you don't get in</sup></sub> | ★★☆ <br> *Medium*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Design Doc](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Flow Code](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Explain YouTube Videos to you like you're 5 </sup></sub> | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Design Doc](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Flow Code](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Cold Opener Generator](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Instant icebreakers that turn cold leads hot </sup></sub> | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Web Search](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Design Doc](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Flow Code](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Want to learn **Agentic Coding**?
  - To setup, read this [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)!
  - Check out [my YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)! Read this [Guide](https://the-pocket.github.io/PocketFlow/guide.html)!
- Want to build your own LLM App? Start with [this template](https://github.com/The-Pocket/PocketFlow-Template-Python)!
