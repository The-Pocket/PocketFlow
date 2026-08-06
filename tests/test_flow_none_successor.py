"""Tests for Flow.get_next_node handling of None successors (issue #56)."""

import unittest
import warnings
from pocketflow import Flow, Node


class TestNoneSuccessor(unittest.TestCase):
    """>> None should create a valid terminal successor without triggering warnings."""

    def test_none_successor_no_warning(self):
        """node - 'end' >> None should not trigger a warning when 'end' is returned."""

        class Decide(Node):
            def exec(self, prep_res):
                return "end"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        decide = Decide()
        decide - "end" >> None

        flow = Flow(start=decide)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = flow.run({})
            flow_warnings = [x for x in w if "Flow ends" in str(x.message)]
            self.assertEqual(len(flow_warnings), 0,
                             f"Unexpected warning: {[str(x.message) for x in flow_warnings]}")
        self.assertEqual(result, "end")

    def test_none_successor_with_other_branches(self):
        """Mixed successors: >> node and >> None should coexist."""

        class Branch(Node):
            def exec(self, prep_res):
                return self.params.get("action", "end")

            def post(self, shared, prep_res, exec_res):
                return exec_res

        class Process(Node):
            def exec(self, prep_res):
                return "processed"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        branch = Branch()
        process = Process()
        branch - "continue" >> process
        branch - "end" >> None

        # Test terminating branch
        flow1 = Flow(start=branch)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result1 = flow1.run({"action": "end"})
            flow_warnings = [x for x in w if "Flow ends" in str(x.message)]
            self.assertEqual(len(flow_warnings), 0)
        self.assertEqual(result1, "end")

        # Test continuing branch
        flow2 = Flow(start=branch)
        flow2.params = {"action": "continue"}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result2 = flow2.run({})
            flow_warnings = [x for x in w if "Flow ends" in str(x.message)]
            # 'processed' is returned by process, which has no successors —
            # that's a legitimate end, no warning expected
            self.assertEqual(len(flow_warnings), 0)
        self.assertEqual(result2, "processed")

    def test_unknown_action_still_warns(self):
        """Returning an action with no registered successor should still warn."""

        class Decide(Node):
            def exec(self, prep_res):
                return "nonexistent"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        class Next(Node):
            pass

        decide = Decide()
        next_node = Next()
        decide - "expected" >> next_node

        flow = Flow(start=decide)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            flow.run({})
            flow_warnings = [x for x in w if "Flow ends" in str(x.message)]
            self.assertEqual(len(flow_warnings), 1)
            self.assertIn("nonexistent", str(flow_warnings[0].message))

    def test_default_none_successor(self):
        """>> None with default action should not warn."""

        class End(Node):
            def exec(self, prep_res):
                return "default"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        end = End()
        end >> None  # default successor is None

        flow = Flow(start=end)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = flow.run({})
            flow_warnings = [x for x in w if "Flow ends" in str(x.message)]
            self.assertEqual(len(flow_warnings), 0)
        self.assertEqual(result, "default")


if __name__ == "__main__":
    unittest.main()
