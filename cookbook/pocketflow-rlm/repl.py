"""A small AST-checked execution environment for the RLM cookbook.

This is intentionally educational. It reduces accidental access to the host
process but is not a substitute for a process/container security boundary.
"""

import ast
import builtins


class RLMExecutionError(ValueError):
    """Raised when generated RLM code violates the cookbook policy."""


_SAFE_BUILTINS = {
    "all": builtins.all,
    "any": builtins.any,
    "enumerate": builtins.enumerate,
    "len": builtins.len,
    "list": builtins.list,
    "max": builtins.max,
    "min": builtins.min,
    "range": lambda *args: _bounded_range(*args),
    "sorted": builtins.sorted,
    "str": builtins.str,
    "sum": builtins.sum,
}
_ALLOWED_CALLS = set(_SAFE_BUILTINS) | {"FINAL", "llm_query", "print"}
_RESERVED_NAMES = {"__builtins__", "FINAL", "context", "llm_query", "print"}
_FORBIDDEN_NODES = (
    ast.Attribute,
    ast.AsyncFunctionDef,
    ast.Await,
    ast.ClassDef,
    ast.Delete,
    ast.FunctionDef,
    ast.Global,
    ast.Import,
    ast.ImportFrom,
    ast.Lambda,
    ast.Nonlocal,
    ast.Raise,
    ast.Try,
    ast.While,
    ast.With,
)


def _bounded_range(*args):
    """Prevent a generated for-loop from allocating an unbounded range."""

    value = range(*args)
    if len(value) > 1000:
        raise RLMExecutionError("range exceeds the 1000-iteration safety limit")
    return value


class _PolicyValidator(ast.NodeVisitor):
    def generic_visit(self, node):
        if isinstance(node, _FORBIDDEN_NODES):
            raise RLMExecutionError(
                f"generated code uses forbidden syntax: {type(node).__name__}"
            )
        super().generic_visit(node)

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_CALLS:
            raise RLMExecutionError("only approved helper calls are allowed")
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) and node.id in _RESERVED_NAMES:
            raise RLMExecutionError(f"cannot overwrite reserved name: {node.id}")
        self.generic_visit(node)


class SafeREPL:
    """Execute one generated program with external context and child calls."""

    def __init__(self, context, llm_query, max_code_chars=8000):
        if max_code_chars <= 0:
            raise ValueError("max_code_chars must be positive")
        self.context = context
        self.llm_query = llm_query
        self.max_code_chars = max_code_chars

    def run(self, code):
        if len(code) > self.max_code_chars:
            raise RLMExecutionError("generated code exceeds max_code_chars")
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as exc:
            raise RLMExecutionError(f"generated code is not valid Python: {exc}") from exc
        _PolicyValidator().visit(tree)

        output = []
        answers = []

        def final(answer):
            answers.append(str(answer))

        def safe_print(*values):
            output.append(" ".join(map(str, values)))
            if sum(len(item) for item in output) > self.max_code_chars:
                raise RLMExecutionError("REPL output exceeds max_code_chars")

        namespace = {
            "__builtins__": _SAFE_BUILTINS,
            "context": self.context,
            "FINAL": final,
            "llm_query": self.llm_query,
            "print": safe_print,
        }
        exec(compile(tree, "<rlm-repl>", "exec"), namespace, namespace)

        if answers:
            return {
                "action": "finish",
                "answer": answers[-1],
                "observation": "\n".join(output),
            }
        return {
            "action": "continue",
            "observation": "\n".join(output) or "The program produced no observation.",
        }


def extract_code(response):
    """Extract one Python block, while accepting a direct ``FINAL(...)`` reply."""

    text = (response or "").strip()
    if "```" in text:
        blocks = text.split("```")
        for block in blocks[1::2]:
            candidate = block.strip()
            first_line, separator, body = candidate.partition("\n")
            if first_line.strip() in {"python", "py"}:
                candidate = body if separator else ""
            if candidate:
                return candidate
    if text.startswith("FINAL("):
        return text
    raise RLMExecutionError("root model must return one Python block or FINAL(...)")
