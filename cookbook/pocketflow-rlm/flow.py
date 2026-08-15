"""Flow assembly for the minimal RLM cookbook."""

from pocketflow import Flow

from nodes import EndNode, REPLNode, RootModelNode


def create_rlm_flow():
    """Create a root-model ↔ REPL loop with a terminal answer transition."""

    root = RootModelNode()
    repl = REPLNode()
    end = EndNode()

    root >> repl
    repl - "continue" >> root
    repl - "finish" >> end

    return Flow(start=root)
