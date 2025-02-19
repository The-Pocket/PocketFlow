<h1 align="center">Pocket Flow - LLM Framework in 100 Lines</h1>



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)

<div align="center">
  <img src="./assets/minillmflow.jpg" width="400"/>
</div>

<br>

A [100-line](pocketflow/__init__.py) minimalist LLM framework for ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Prompt Chaining](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

- Install via  ```pip install pocketflow```, or just copy the [source codes](pocketflow/__init__.py) (only 100 lines)

- If the 100 lines feel terse and you’d prefer a friendlier intro, [check this out](https://chatgpt.com/share/678564bd-1ba4-8000-98e4-a6ffe363c1b8)

- **💡 Pro tip!!** Build LLM apps with LLMs assistants (ChatGPT, Claude, Cursor.ai, etc.)

  <details>
    <summary><b>(🫵 Click to expand) Use Claude to build LLM apps</b></summary>

    - Create a [project](https://www.anthropic.com/news/projects) and upload the [docs](docs) to project knowledge
  
    - Set project custom instructions. For example:
      ```
      1. check "tool.md" and "llm.md" for the required functions.
      2. design the high-level (batch) flow and nodes in artifact using mermaid
      3. design the shared memory structure: define its fields, data structures, and how they will be updated.
      Think out aloud for above first and ask users if your design makes sense.
      4. Finally, implement. Start with simple, minimalistic codes without, for example, typing. Write the codes in artifact.
      ```
    - Ask it to build LLM apps (Sonnet 3.5 strongly recommended)!
      ```
      Help me build a chatbot based on a directory of PDFs.
      ```
 
      <div align="center">
        <img src="./assets/claude_project.gif"/>
      </div>
  </details>

  <details>
    <summary><b>(🫵 Click to expand) Use ChatGPT to build LLM apps</b></summary>

    - Try the [GPT assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant). However, it uses older models, which are good for explaining but not that good at coding.

      <div align="center">
        <img src="./assets/gpt_store.gif"/>
      </div>

    - For stronger coding capabilities, consider sending the [docs](docs) to more advanced models like O1.
  
        - Paste the docs link (https://github.com/the-pocket/PocketFlow/tree/main/docs) to [Gitingest](https://gitingest.com/).

        - Then, paste the generated contents into your O1 prompt, and ask it to build LLM apps.
     
    
  </details>


Documentation: https://the-pocket.github.io/PocketFlow/

## Why Pocket Flow?

Pocket Flow is designed to be **the framework used by LLMs**. In the future, LLM projects will be *self-programmed* by LLMs themselves: Users specify requirements, and LLMs will design, build, and maintain. Current LLMs are:

1. **👍 Good at Low-level Details:** LLMs can handle details like *wrappers, tools, and prompts*, which don't belong in a framework. Current frameworks are over-engineered, making them hard for humans (and LLMs) to maintain.

2. **👎 Bad at High-level Paradigms:** While paradigms like *MapReduce, Task Decomposition, and Agents* are powerful, LLMs still struggle to design them elegantly. These high-level concepts should be emphasized in frameworks.

The ideal framework for LLMs should (1) **strip away low-level implementation details**, and (2) **keep high-level programming paradigms**. Hence, we provide this minimal (100-line) framework that allows LLMs to focus on what matters.  

Pocket Flow is also a *learning resource*, as current frameworks abstract too much away.

| Framework      | Computation Models | Communication Models | App-Specific Models                                    | Vendor-Specific Models                                   | Lines Of Codes            | Package + Dependency Size         |
|:--------------:|:------------------:|:--------------------:|:-------------------------------------------------------:|:--------------------------------------------------------:|:-----------------:|:---------------------------:|
| LangChain      | Agent, Chain       | Message              | Many                       | Many                          | *405K*            | *+166MB*                    |
| CrewAI         | Agent, Chain       | Message, Shared      | Many              | Many               | *18K*             | *+173MB*                    |
| SmolAgent      | Agent              | Message              | Some              | Some              | *8K*              | *+198MB*                    |
| LangGraph      | Agent, Graph       | Message, Shared      | Some                          | Some                  | *37K*             | *+51MB*                     |
| AutoGen        | Agent              | Message              | Some                   | Many             | *7K*  | *+26MB*         |
| **PocketFlow** | **Graph**          | **Shared**           | **None**                                                | **None**                                                | **100**           | **+56KB**                   |


## How Does it Work?

The [100 lines](pocketflow/__init__.py) capture what we see as the core abstraction of most LLM frameworks: **Nested Directed Graph** that breaks down tasks into multiple (LLM) steps, with branching and recursion for agent-like decision-making. 

<div align="center">
  <img src="./assets/abstraction.png" width="700"/>
</div>

From there, it’s easy to layer on more complex features like ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Prompt Chaining](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

<div align="center">
  <img src="./assets/paradigm.png" width="700"/>
</div>

- To learn more details, please check out documentation: https://the-pocket.github.io/PocketFlow/

- Beginner Tutorial: [Text summarization for Paul Graham Essay + QA agent](https://colab.research.google.com/github/the-pocket/PocketFlow/blob/main/cookbook/demo.ipynb)
 
- More coming soon ... Let us know you’d love to see!


