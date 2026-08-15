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
from nodes import PrepareContextNode  # noqa: E402


class RLMFlowTests(unittest.TestCase):
    def test_prepare_context_bounds_chunks(self):
        shared = {"document": "abcdefghij", "chunk_size": 4}
        PrepareContextNode().run(shared)
        self.assertEqual(shared["chunks"], ["abcd", "efgh", "ij"])

    def test_flow_recursively_compresses_without_network(self):
        prompts = []

        def fake_llm(prompt):
            prompts.append(prompt)
            if prompt.startswith("Summarize"):
                return "summary-" + prompt.split("Context chunk:\n", 1)[1][:4]
            return "final answer"

        shared = {
            "document": "abcdefghij",
            "question": "What is this?",
            "chunk_size": 3,
            "max_context_chars": 12,
            "max_levels": 3,
        }
        with patch("nodes.call_llm", side_effect=fake_llm):
            create_rlm_flow().run(shared)

        self.assertEqual(shared["answer"], "final answer")
        self.assertGreaterEqual(len(prompts), 4)
        self.assertLessEqual(shared["level"], shared["max_levels"])


if __name__ == "__main__":
    unittest.main()
