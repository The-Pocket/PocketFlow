from pocketflow import Flow
from nodes import (CompactHistory, DecideAction, ListFiles, GrepSearch,
                   ReadFile, RunCommand, PatchRead, PatchValidate, PatchApply)

def create_coding_agent_flow():
    # Patch subflow (Flow IS Node pattern)
    pr, pv, pa = PatchRead(), PatchValidate(), PatchApply()
    pr >> pv >> pa

    class PatchFile(Flow):
        def __init__(self): super().__init__(start=pr)
        def post(self, shared, prep_res, exec_res):
            result = shared.pop("_patch_result", "ERROR: validation failed")
            shared.setdefault("history", []).append({
                "tool": "patch_file",
                "args": shared["tool_call"].get("args", {}),
                "result": result,
            })
            print(f"  ✍️ {result[:200]}")

    compact = CompactHistory()
    decide = DecideAction(max_retries=3)

    decide - "retry" >> compact
    decide - "list_files" >> ListFiles() >> compact
    decide - "grep_search" >> GrepSearch() >> compact
    decide - "read_file" >> ReadFile() >> compact
    decide - "patch_file" >> PatchFile() >> compact
    decide - "run_command" >> RunCommand() >> compact
    compact >> decide

    return Flow(start=compact)
