import os, subprocess, re, json, difflib
from pocketflow import Node, Flow
from utils import call_llm

# Constants
MAX_STEPS = 50
COMPACT_AFTER = 30

# Utilities
def _path(workdir, p): return os.path.join(workdir, p)

def load_memory(workdir):
    memory_file = os.path.join(workdir, ".memory.md")
    if os.path.exists(memory_file):
        with open(memory_file) as f: return f.read()
    return ""

def save_memory(workdir, history):
    memory_file = os.path.join(workdir, ".memory.md")
    summary = call_llm(
        "Summarize key learnings from this coding session in 2-3 bullets:\n"
        + "\n".join(f"- {h['tool']}: {h['result']}" for h in history[-5:])
    )
    with open(memory_file, "w") as f: f.write(summary)

def load_skills(workdir):
    p = os.path.join(workdir, "AGENTS.md")
    if os.path.exists(p):
        with open(p) as f: return f.read()
    return ""

TOOL_DESC = """- list_files(directory='.') — List all files
- grep_search(pattern, path='.') — Search for pattern in .py files
- read_file(path, start=1, end=None) — Read file with line numbers
- patch_file(path, old_str, new_str) — Replace old_str with new_str
- run_command(cmd) — Run shell command
- done(result) — Task complete"""

VALID_TOOLS = {"list_files", "grep_search", "read_file", "patch_file", "run_command"}

class CompactHistory(Node):
    def prep(self, shared):
        return shared.get("history", []), shared["task"]
    def exec(self, inputs):
        history, task = inputs
        if len(history) <= COMPACT_AFTER: return history
        old = history[:len(history) - COMPACT_AFTER // 2]
        recent = history[len(history) - COMPACT_AFTER // 2:]
        old_text = "\n".join(f"- {h['tool']}: {h['result']}" for h in old)
        summary = call_llm(f"Summarize these past actions briefly:\n{old_text}")
        return [{"tool": "summary", "args": {}, "result": summary}] + recent
    def post(self, shared, prep_res, exec_res):
        shared["history"] = exec_res

class DecideAction(Node):
    def prep(self, shared):
        history = shared.get("history", [])
        workdir = shared["workdir"]
        skills = load_skills(workdir)
        memory = load_memory(workdir)
        history_text = ""
        for h in history:
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in h.get("args", {}).items())
            history_text += f"\n[{h['tool']}({args_str})]\n{h['result']}\n"
        parts = ["You are a coding agent. Your job: fix failing tests."]
        if skills:
            parts.append(f"Project rules:\n{skills}")
        if memory:
            parts.append(f"Memory from past sessions:\n{memory}")
        parts.append(f"Available tools:\n{TOOL_DESC}")
        parts.append(f"Task: {shared['task']}")
        parts.append(f"History:{history_text or ' (none yet — start by running the tests)'}")
        parts.append('Pick ONE tool. Output ONLY json:\n```json\n{"tool": "tool_name", "args": {"arg1": "value1"}, "reason": "why"}\n```')
        return "\n\n".join(parts)
    def exec(self, prompt):
        resp = call_llm(prompt)
        json_str = resp.split("```json")[1].split("```")[0].strip()
        parsed = json.loads(json_str)
        assert "tool" in parsed
        return parsed
    def post(self, shared, prep_res, exec_res):
        tool = exec_res.get("tool", "done")
        step = shared.get("step", 0) + 1
        shared["step"] = step
        if tool == "done" or step >= MAX_STEPS:
            shared["result"] = exec_res.get("result", exec_res.get("args", {}).get("result", ""))
            if shared.get("history"): save_memory(shared["workdir"], shared["history"])
            return "done"
        print(f"  🔧 [{step}] {tool} — {exec_res.get('reason', '')}")
        shared["tool_call"] = exec_res
        if tool not in VALID_TOOLS:
            shared.setdefault("history", []).append({
                "tool": tool, "args": {}, "result": f"Unknown tool '{tool}'. Use: {', '.join(VALID_TOOLS)}"
            })
            return "retry"
        return tool

class ToolNode(Node):
    def prep(self, shared):
        return shared["tool_call"].get("args", {}), shared["workdir"]
    def post(self, shared, prep_res, exec_res):
        shared.setdefault("history", []).append({
            "tool": shared["tool_call"]["tool"],
            "args": shared["tool_call"].get("args", {}),
            "result": str(exec_res),
        })
        print(f"  ✅ {str(exec_res)[:200]}")

class ListFiles(ToolNode):
    def exec(self, inputs):
        args, workdir = inputs
        result = []
        for root, _, files in os.walk(_path(workdir, args.get("directory", "."))):
            for f in files:
                if not f.startswith("."): result.append(os.path.relpath(os.path.join(root, f), workdir))
        return "\n".join(result)

class GrepSearch(ToolNode):
    def exec(self, inputs):
        args, workdir = inputs
        pattern, path = args.get("pattern", ""), args.get("path", ".")
        results = []
        for root, _, files in os.walk(_path(workdir, path)):
            for fname in files:
                if not fname.endswith(".py"): continue
                fpath = os.path.join(root, fname)
                with open(fpath) as f:
                    for i, line in enumerate(f, 1):
                        if re.search(pattern, line):
                            results.append(f"{os.path.relpath(fpath, workdir)}:{i}: {line.rstrip()}")
        return "\n".join(results) or "No matches"

class ReadFile(ToolNode):
    def exec(self, inputs):
        args, workdir = inputs
        with open(_path(workdir, args["path"])) as f: lines = f.readlines()
        end = args.get("end") or len(lines)
        start = args.get("start", 1)
        return "".join(f"{i}: {l}" for i, l in enumerate(lines[start-1:end], start))

class RunCommand(ToolNode):
    def exec(self, inputs):
        args, workdir = inputs
        r = subprocess.run(args["cmd"], shell=True, capture_output=True, text=True, cwd=workdir, timeout=30)
        return (r.stdout + r.stderr) or "(no output)"

# patch_file as SubFlow
class PatchRead(Node):
    def prep(self, shared):
        return shared["tool_call"]["args"]["path"], shared["workdir"]
    def exec(self, inputs):
        path, workdir = inputs
        with open(_path(workdir, path)) as f: return f.read()
    def post(self, shared, prep_res, exec_res):
        shared["_patch_content"] = exec_res

class PatchValidate(Node):
    def prep(self, shared):
        args = shared["tool_call"]["args"]
        return shared["_patch_content"], args["old_str"], args["path"]
    def exec(self, inputs):
        content, old_str, path = inputs
        if old_str not in content:
            lines = content.split('\n')
            n = old_str.count('\n') + 1
            chunks = ['\n'.join(lines[i:i+n]) for i in range(len(lines))]
            best = difflib.get_close_matches(old_str, chunks, n=1, cutoff=0.4)
            if best: return f"ERROR: old_str not found in {path}. Did you mean:\n{best[0]}"
            return f"ERROR: old_str not found in {path}"
        if content.count(old_str) > 1:
            return f"ERROR: old_str appears {content.count(old_str)} times. Include more context."
        return "ok"
    def post(self, shared, prep_res, exec_res):
        if exec_res != "ok":
            shared["_patch_result"] = exec_res
            return "error"

class PatchApply(Node):
    def prep(self, shared):
        args = shared["tool_call"]["args"]
        return shared["_patch_content"], args["old_str"], args["new_str"], args["path"], shared["workdir"]
    def exec(self, inputs):
        content, old_str, new_str, path, workdir = inputs
        with open(_path(workdir, path), "w") as f: f.write(content.replace(old_str, new_str, 1))
        return f"Patched {path}"
    def post(self, shared, prep_res, exec_res):
        shared["_patch_result"] = exec_res
