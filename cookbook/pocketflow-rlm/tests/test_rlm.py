import sys
import unittest
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve()
COOKBOOK = HERE.parents[1]
REPO = COOKBOOK.parents[1]
sys.path.insert(0, str(COOKBOOK))
sys.path.insert(0, str(REPO))

from flow import create_rlm_flow  # noqa: E402
from repl import RLMExecutionError, SafeREPL  # noqa: E402


class RLMFlowTests(unittest.TestCase):
    def test_repl_keeps_context_external_and_calls_child(self):
        child_prompts = []

        def child(prompt):
            child_prompts.append(prompt)
            return "child found the relevant fact"

        repl = SafeREPL("secret context", child)
        result = repl.run(
            "excerpt = context[:6]\n"
            "print(llm_query('Review this excerpt: ' + excerpt))\n"
            "FINAL('done')"
        )

        self.assertEqual(result["action"], "finish")
        self.assertEqual(result["answer"], "done")
        self.assertEqual(child_prompts, ["Review this excerpt: secret"])

    def test_repl_rejects_imports_and_unbounded_while(self):
        repl = SafeREPL("context", lambda prompt: "unused")
        for code in (
            "import os",
            "while True:\n    pass",
            "context = 'overwritten'",
        ):
            with self.assertRaises(RLMExecutionError):
                repl.run(code)

    def test_flow_keeps_full_context_out_of_root_prompt(self):
        root_prompts = []
        sub_prompts = []

        def fake_llm(prompt):
            if prompt.startswith("ROOT"):
                root_prompts.append(prompt)
                if len(root_prompts) == 1:
                    return "```python\nprint(llm_query('Find the answer in: ' + context[:5]))\n```"
                return "```python\nFINAL('answer from child evidence')\n```"
            self.assertTrue(prompt.startswith("SUBMODEL RLM QUERY"))
            sub_prompts.append(prompt)
            return "child evidence"

        context = "PRIVATE-CONTEXT-" + ("x" * 500)
        shared = {
            "context": context,
            "question": "What is the answer?",
            "max_iterations": 3,
        }
        with patch("nodes.call_llm", side_effect=fake_llm):
            create_rlm_flow().run(shared)

        self.assertEqual(shared["answer"], "answer from child evidence")
        self.assertEqual(len(root_prompts), 2)
        self.assertEqual(len(sub_prompts), 1)
        for prompt in root_prompts:
            self.assertNotIn(context, prompt)
        self.assertIn("PRIVA", sub_prompts[0])

    def test_flow_reports_invalid_program_and_allows_recovery(self):
        root_calls = []

        def recoverable(prompt):
            if prompt.startswith("ROOT"):
                root_calls.append(prompt)
                if len(root_calls) == 1:
                    return "```python\nimport os\n```"
                return "```python\nFINAL('recovered')\n```"
            return "unused"

        shared = {
            "context": "context",
            "question": "question",
            "max_iterations": 3,
        }
        with patch("nodes.call_llm", side_effect=recoverable):
            create_rlm_flow().run(shared)

        self.assertEqual(shared["answer"], "recovered")
        self.assertEqual(len(root_calls), 2)
        self.assertIn("RLMExecutionError", shared["observations"][0])

    def test_flow_stops_when_root_never_finishes(self):
        root_calls = []

        def never_finish(prompt):
            if prompt.startswith("ROOT"):
                root_calls.append(prompt)
                return "```python\nprint('still working')\n```"
            return "unused"

        shared = {
            "context": "context",
            "question": "question",
            "max_iterations": 2,
        }
        with patch("nodes.call_llm", side_effect=never_finish):
            create_rlm_flow().run(shared)

        self.assertEqual(len(root_calls), 2)
        self.assertIn("max_iterations", shared["answer"])


if __name__ == "__main__":
    unittest.main()
