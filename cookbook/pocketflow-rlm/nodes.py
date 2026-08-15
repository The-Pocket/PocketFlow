"""Nodes for a small Recursive Language Model (RLM) cookbook.

The workflow keeps the long document in shared state and only sends bounded
chunks (or recursively compressed summaries) to the language model.
"""

from pocketflow import BatchNode, Node
from utils import call_llm


class PrepareContextNode(Node):
    """Split a document into bounded, non-empty chunks."""

    def prep(self, shared):
        return shared["document"], shared.get("chunk_size", 4000)

    def exec(self, inputs):
        document, chunk_size = inputs
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        return [document[i : i + chunk_size] for i in range(0, len(document), chunk_size)]

    def post(self, shared, prep_res, exec_res):
        shared["chunks"] = exec_res
        shared["level"] = 0


class SummarizeChunksNode(BatchNode):
    """Map one bounded prompt over every current context chunk."""

    def prep(self, shared):
        return shared.get("chunks", [])

    def exec(self, chunk):
        return call_llm(
            "Summarize the following context chunk. Preserve names, numbers, "
            "and decisions that may be needed to answer the user's question.\n\n"
            f"Context chunk:\n{chunk}"
        )

    def post(self, shared, prep_res, exec_res):
        shared["summaries"] = exec_res


class ReduceOrFinishNode(Node):
    """Recursively compress summaries until they fit, then answer the query."""

    def prep(self, shared):
        return (
            shared.get("summaries", []),
            shared["question"],
            shared.get("max_context_chars", 6000),
            shared.get("max_levels", 3),
            shared.get("level", 0),
        )

    def exec(self, inputs):
        summaries, question, max_context_chars, max_levels, level = inputs
        combined = "\n\n---\n\n".join(summaries)
        if len(combined) <= max_context_chars or level >= max_levels:
            return {
                "action": "finish",
                "answer": call_llm(
                    "Answer the question using only the context below. "
                    "If the context is insufficient, say so explicitly.\n\n"
                    f"Question: {question}\n\nContext:\n{combined}"
                ),
            }

        next_chunks = [
            combined[i : i + max_context_chars]
            for i in range(0, len(combined), max_context_chars)
        ]
        return {"action": "recurse", "chunks": next_chunks}

    def post(self, shared, prep_res, exec_res):
        if exec_res["action"] == "recurse":
            shared["chunks"] = exec_res["chunks"]
            shared["level"] = prep_res[-1] + 1
            return "recurse"
        shared["answer"] = exec_res["answer"]
        return "finish"


class EndNode(Node):
    """Explicit terminal node so the flow can finish without a warning."""

    def exec(self, _):
        return None
