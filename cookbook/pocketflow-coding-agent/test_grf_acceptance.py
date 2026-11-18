"""Focused tests for the optional GRF gate (stdlib unittest only)."""
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

# The gate itself uses stdlib APIs; keep this test independent of the example's
# optional PocketFlow/OpenAI runtime dependencies.
pocketflow = types.ModuleType("pocketflow")
pocketflow.Node = type("Node", (), {})
pocketflow.Flow = type("Flow", (), {})
sys.modules.setdefault("pocketflow", pocketflow)
utils = types.ModuleType("utils")
utils.call_llm = lambda *_args, **_kwargs: ""
sys.modules.setdefault("utils", utils)

from nodes import complete_grf_task


class GrfAcceptanceTests(unittest.TestCase):
    def test_failed_check_does_not_attempt_completion(self):
        failed = types.SimpleNamespace(returncode=1, stdout='{"result":"FAIL"}', stderr="")
        with patch("nodes.subprocess.run", return_value=failed) as run:
            passed, message = complete_grf_task("/project", "finished")
        self.assertFalse(passed)
        self.assertIn("task remains active", message)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0][-2:], ["grf.py", "check"])

    def test_passing_check_completes_with_its_receipt(self):
        with tempfile.TemporaryDirectory() as project:
            receipt = Path(project, ".grf", "receipts", "pass.json")
            receipt.parent.mkdir(parents=True)
            receipt.write_text("{}", encoding="utf-8")
            check = types.SimpleNamespace(
                returncode=0,
                stdout=json.dumps({"result": "PASS", "receipt": ".grf/receipts/pass.json"}),
                stderr="",
            )
            complete = types.SimpleNamespace(returncode=0, stdout="completed", stderr="")
            with patch("nodes.subprocess.run", side_effect=[check, complete]) as run:
                passed, message = complete_grf_task(project, "all tests pass")
            self.assertTrue(passed)
            self.assertEqual(message, "completed")
            command = run.call_args_list[1].args[0]
            self.assertEqual(command[1:4], ["grf.py", "session", "complete"])
            self.assertEqual(command[command.index("--evidence") + 1], ".grf/receipts/pass.json")
            self.assertEqual(command[command.index("--summary") + 1], "all tests pass")


if __name__ == "__main__":
    unittest.main()
