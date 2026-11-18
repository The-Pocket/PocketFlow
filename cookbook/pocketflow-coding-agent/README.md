# Coding Agent

A production-ready coding agent built with PocketFlow that autonomously implements skeleton code to make failing tests pass. It uses an LLM-driven tool loop with 6 tools, persistent memory across sessions, and project-specific skills loading.

## Features

- **6 Tools**: `list_files`, `grep_search`, `read_file`, `patch_file`, `run_command`, `done`
- **Memory**: Saves learnings from past sessions to `.memory.md` for future runs
- **Skills**: Loads project-specific rules from `AGENTS.md` if present
- **Patch SubFlow**: `patch_file` implemented as a Flow-IS-Node SubFlow (Read -> Validate -> Apply) with fuzzy matching for error recovery
- **History Compaction**: Automatically summarizes long histories to stay within context limits
- **One Node Per Tool**: Clean routing architecture with dedicated nodes for each tool

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Export your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key-here
```

3. Test the LLM connection:
```bash
python utils/call_llm.py
```

4. Run the coding agent:
```bash
python main.py
```

The agent will create a test project with a mini SQL engine (tokenizer, parser, executor) and autonomously implement all skeleton functions to make the tests pass.

## How It Works

```mermaid
graph TD
    Start[CompactHistory] --> Decide[DecideAction]
    Decide -->|list_files| LF[ListFiles] --> Start
    Decide -->|grep_search| GS[GrepSearch] --> Start
    Decide -->|read_file| RF[ReadFile] --> Start
    Decide -->|patch_file| PF[PatchFile SubFlow] --> Start
    Decide -->|run_command| RC[RunCommand] --> Start
    Decide -->|retry| Start
    Decide -->|done| End[Done]

    subgraph PatchFile SubFlow
        PR[PatchRead] --> PV[PatchValidate]
        PV --> PA[PatchApply]
        PV -->|error| EX[Return Error]
    end
```

The agent operates in a loop:
1. **CompactHistory** compresses old history entries to avoid context overflow
2. **DecideAction** sends the task, history, memory, and skills to the LLM, which picks one tool
3. The chosen **tool node** executes the action and records the result
4. Loop back to step 1 until the LLM calls `done` or max steps reached

## Optional GRF acceptance gate

The default `python main.py` behavior is unchanged. To require a GRF acceptance
check before this agent treats the model's `done` response as complete, first
initialize GRF in the generated `test_project` and sign in a task there. Keep
the example's existing project check in GRF: configure the GRF acceptance
check to run the same command used above,
`python -m pytest test_tokenizer.py test_parser.py test_executor.py -v`,
from `test_project` (for example, have `checks/acceptance.py` invoke that argv
with `subprocess.run(..., cwd=project_root, check=True)`). Do not replace the
project test command with an unrelated GRF-only check.

Then run the agent with the opt-in flag:

```bash
python setup_test_project.py
python /path/to/grf_starter.py init --intent "Implement the mini SQL engine and pass its tests" test_project
cd test_project
python grf.py session sign-in --task "Implement the mini SQL engine and pass its tests"
cd ..
python main.py --grf-acceptance
```

When the model says `done`, the agent runs the project-local `python grf.py
check`. A failing check is appended to its history and the active GRF task is
left open so the agent can repair the project. A passing check must include a
real receipt; the agent passes that receipt and its result summary to the
project-local `session complete` command. If GRF completion is rejected, the
agent does not treat the task as complete. This is cooperative workflow
gating, not a security boundary or proof that the checks are well designed.

## Files

| File | Description |
|------|-------------|
| `main.py` | Entry point — sets up test project and runs the agent |
| `flow.py` | Defines the agent flow with tool routing and PatchFile SubFlow |
| `nodes.py` | All node implementations (CompactHistory, DecideAction, tool nodes, patch SubFlow) |
| `utils/call_llm.py` | OpenAI GPT-4o wrapper |
| `setup_test_project.py` | Creates a mini SQL engine project with skeleton code and tests |
| `requirements.txt` | Python dependencies |

## Example Output

```
🤖 Coding Agent starting...
📋 Task: Implement the skeleton functions to make all tests pass.
📁 Working in: test_project/

  🔧 [1] run_command — Run the tests to see what's failing
  ✅ 20 passed, 48 failed

  🔧 [2] read_file — Read db.py to understand the skeleton
  ✅ (file contents displayed)

  🔧 [3] patch_file — Implement parse_select()
  ✍️ Patched db.py

  🔧 [4] patch_file — Implement parse_select_columns()
  ✍️ Patched db.py

  ...

  🔧 [15] run_command — Run tests again
  ✅ 68 passed, 0 failed

  🔧 [16] done — All tests pass!

🎯 Result: All 68 tests pass. Implemented parser and executor functions.
```
