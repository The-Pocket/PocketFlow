"""Regression tests for the optional GRF gate on the real PocketFlow Node."""
import sys
import unittest
from unittest.mock import patch

# Import the repository's real PocketFlow Node class. GRF behavior itself is
# exercised by the isolated adoption smoke test; these tests isolate the node's
# boundary decision while mocking only its GRF result and external LLM call.
from pocketflow import Node

import nodes


class GrfAcceptanceTests(unittest.TestCase):
    def test_decide_action_is_a_real_pocketflow_node(self):
        self.assertTrue(issubclass(nodes.DecideAction, Node))

    def test_failed_check_with_budget_returns_retry_and_keeps_failure_in_history(self):
        shared = {"workdir": "/unused", "grf_acceptance": True, "history": [], "step": 0}
        with patch("nodes.complete_grf_task", return_value=(False, "checks failed; task remains active")):
            action = nodes.DecideAction().post(shared, None, {"tool": "done", "result": "finished"})
        self.assertEqual(action, "retry")
        self.assertIn("checks failed", shared["history"][-1]["result"])
        self.assertEqual(shared["result"], "checks failed; task remains active")

    def test_done_at_step_limit_raises_non_success_on_failed_check(self):
        shared = {"workdir": "/unused", "grf_acceptance": True, "history": [], "step": nodes.MAX_STEPS - 1}
        with patch("nodes.complete_grf_task", return_value=(False, "checks failed")):
            with self.assertRaises(nodes.GrfAcceptanceError):
                nodes.DecideAction().post(shared, None, {"tool": "done", "result": "finished"})
        self.assertIn("checks failed", shared["result"])

    def test_regular_tool_at_step_limit_raises_non_success_on_failed_check(self):
        shared = {"workdir": "/unused", "grf_acceptance": True, "history": [], "step": nodes.MAX_STEPS - 1}
        with patch("nodes.complete_grf_task", return_value=(False, "checks failed")):
            with self.assertRaises(nodes.GrfAcceptanceError):
                nodes.DecideAction().post(shared, None, {"tool": "run_command"})
        self.assertIn("checks failed", shared["result"])

    def test_passed_check_allows_done(self):
        shared = {"workdir": "/unused", "grf_acceptance": True, "history": [], "step": nodes.MAX_STEPS - 1}
        with patch("nodes.complete_grf_task", return_value=(True, "completed")):
            action = nodes.DecideAction().post(shared, None, {"tool": "done", "result": "finished"})
        self.assertEqual(action, "done")
        self.assertEqual(shared["result"], "finished")

    def test_default_done_path_is_unchanged(self):
        shared = {"workdir": "/unused", "history": [], "step": 0}
        with patch("nodes.complete_grf_task") as grf:
            action = nodes.DecideAction().post(shared, None, {"tool": "done", "result": "finished"})
        self.assertEqual(action, "done")
        grf.assert_not_called()


if __name__ == "__main__":
    unittest.main()
