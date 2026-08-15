"""PocketFlow nodes for a minimal Recursive Language Model (RLM)."""

from pocketflow import Node

from repl import SafeREPL, extract_code
from utils import call_llm


def _root_prompt(question, context_length, observations, iteration, max_iterations):
    """Build a bounded root-model prompt without embedding the full context."""

    history = ("\n\n".join(observations[-5:]) or "(no observations yet)")[-12000:]
    final_hint = (
        "You must call FINAL(answer) in this turn."
        if iteration >= max_iterations - 1
        else ""
    )
    return f"""ROOT RLM INSTRUCTION
You are the root model in a Recursive Language Model workflow.
The full input is an external Python string named `context`; it is not included
in this prompt. Inspect it with slices, and delegate focused questions to
`llm_query(prompt)`. The helper calls a child language model and returns text.
You may use `len`, `range`, `enumerate`, slicing, string concatenation, and
`print`. Do not import modules or access the filesystem/network.

Question: {question}
Context length: {context_length} characters
Iteration: {iteration}/{max_iterations}
Previous observations:
{history}

Return exactly one Python code block. Use `FINAL(answer)` when you have enough
evidence; otherwise inspect a new context slice or call `llm_query(...)` and
print the useful result. {final_hint}
"""


class RootModelNode(Node):
    """Ask the root model for the next REPL program."""

    def prep(self, shared):
        context = shared["context"]
        return (
            shared["question"],
            len(context),
            shared.get("observations", []),
            shared.get("iteration", 0),
            shared.get("max_iterations", 6),
        )

    def exec(self, inputs):
        question, context_length, observations, iteration, max_iterations = inputs
        if max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        return call_llm(
            _root_prompt(
                question,
                context_length,
                observations,
                iteration,
                max_iterations,
            )
        )

    def post(self, shared, prep_res, exec_res):
        shared["root_response"] = exec_res
        shared["iteration"] = prep_res[-2] + 1


class REPLNode(Node):
    """Execute one root-model program and expose bounded recursive sub-calls."""

    def prep(self, shared):
        return (
            shared["root_response"],
            shared["context"],
            shared["question"],
            shared.get("max_code_chars", 8000),
        )

    def exec(self, inputs):
        response, context, question, max_code_chars = inputs

        code = extract_code(response)
        sub_calls = []

        def llm_query(prompt):
            if len(prompt) > max_code_chars:
                raise ValueError("llm_query prompt exceeds max_code_chars")
            if len(sub_calls) >= 32:
                raise ValueError("per-iteration llm_query limit exceeded")
            sub_calls.append(prompt)
            return call_llm(
                "SUBMODEL RLM QUERY\n"
                "Answer the focused question from the supplied excerpt only.\n\n"
                f"Question: {question}\n\n"
                f"{prompt}"
            )

        repl = SafeREPL(
            context=context,
            llm_query=llm_query,
            max_code_chars=max_code_chars,
        )
        try:
            result = repl.run(code)
        except Exception as exc:
            result = {
                "action": "continue",
                "observation": (
                    f"REPL execution error: {type(exc).__name__}: {exc}"
                ),
            }
        result["sub_calls"] = sub_calls
        return result

    def post(self, shared, prep_res, exec_res):
        observation = exec_res.get("observation", "")
        if exec_res.get("sub_calls"):
            observation = (
                f"Performed {len(exec_res['sub_calls'])} sub-model call(s).\n"
                + observation
            )
        shared.setdefault("observations", []).append(observation[:8000])
        if exec_res["action"] == "finish":
            shared["answer"] = exec_res["answer"]
            return "finish"
        if shared["iteration"] >= shared.get("max_iterations", 6):
            shared["answer"] = (
                "The RLM reached max_iterations without producing a FINAL answer."
            )
            return "finish"
        return "continue"


class EndNode(Node):
    """Explicit terminal node for the PocketFlow graph."""

    def exec(self, _):
        return None
