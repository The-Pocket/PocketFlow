# tests/test_flow_basic.py
import sys
import unittest
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Flow, Node

# --- Node Definitions ---
# Nodes intended for default transitions (>>) should NOT return a specific
# action string from post. Let it return None by default.
# Nodes intended for conditional transitions (-) MUST return the action string.

class NumberNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] = self.number
    # post implicitly returns None - used for default transition

class AddNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] += self.number
    # post implicitly returns None - used for default transition

class MultiplyNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] *= self.number
    # post implicitly returns None - used for default transition

class CheckPositiveNode(Node):
   # This node IS designed for conditional branching
   def prep(self, shared):
       pass
   def post(self, shared, prep_res, exec_res):
        # MUST return the specific action string for branching
        if shared['current'] >= 0:
            return 'positive'
        else:
            return 'negative'

class NoOpNode(Node):
    # Just a placeholder node
    pass # post implicitly returns None

class EndSignalNode(Node):
    # A node specifically to return a value when it's the end
    def __init__(self, signal="finished"):
        super().__init__()
        self.signal = signal
    def post(self, shared, prep_res, exec_res):
        return self.signal # Return a specific signal

# --- Test Class ---
class TestFlowBasic(unittest.TestCase):

    def test_start_method_initialization(self):
        """Test initializing flow with start() after creation."""
        shared = {}
        n1 = NumberNode(5)
        pipeline = Flow()
        pipeline.start(n1)
        last_action = pipeline.run(shared=shared)
        self.assertEqual(shared['current'], 5)
        # NumberNode.post returns None (default)
        self.assertIsNone(last_action)

    def test_start_method_chaining(self):
        """Test fluent chaining using start().next()..."""
        shared = {}
        pipeline = Flow()
        # Chain: NumberNode -> AddNode -> MultiplyNode
        # All use default transitions (post returns None)
        pipeline.start(NumberNode(5)).next(AddNode(3)).next(MultiplyNode(2))
        last_action = pipeline.run(shared=shared)
        self.assertEqual(shared['current'], 16)
        # Last node (MultiplyNode) post returns None
        self.assertIsNone(last_action)

    def test_sequence_with_rshift(self):
        """Test a simple linear pipeline using >>"""
        shared = {}
        n1 = NumberNode(5)
        n2 = AddNode(3)
        n3 = MultiplyNode(2)

        pipeline = Flow()
        # All default transitions (post returns None)
        pipeline.start(n1) >> n2 >> n3

        last_action = pipeline.run(shared)
        self.assertEqual(shared['current'], 16)
        # Last node (n3: MultiplyNode) post returns None
        self.assertIsNone(last_action)

    def test_branching_positive(self):
        """Test positive branch: CheckPositiveNode returns 'positive'"""
        shared = {}
        start_node = NumberNode(5)    # post -> None
        check_node = CheckPositiveNode() # post -> 'positive' or 'negative'
        add_if_positive = AddNode(10) # post -> None
        add_if_negative = AddNode(-20) # post -> None (won't run)

        pipeline = Flow()
        # start -> check (default); check branches on 'positive'/'negative'
        pipeline.start(start_node) >> check_node
        check_node - "positive" >> add_if_positive
        check_node - "negative" >> add_if_negative

        # Execution: start_node -> check_node -> add_if_positive
        last_action = pipeline.run(shared)
        self.assertEqual(shared['current'], 15) # 5 + 10
        # Last node executed was add_if_positive, its post returns None
        self.assertIsNone(last_action)

    def test_branching_negative(self):
        """Test negative branch: CheckPositiveNode returns 'negative'"""
        shared = {}
        start_node = NumberNode(-5)   # post -> None
        check_node = CheckPositiveNode() # post -> 'positive' or 'negative'
        add_if_positive = AddNode(10) # post -> None (won't run)
        add_if_negative = AddNode(-20) # post -> None

        pipeline = Flow()
        pipeline.start(start_node) >> check_node
        check_node - "positive" >> add_if_positive
        check_node - "negative" >> add_if_negative

        # Execution: start_node -> check_node -> add_if_negative
        last_action = pipeline.run(shared)
        self.assertEqual(shared['current'], -25) # -5 + -20
        # Last node executed was add_if_negative, its post returns None
        self.assertIsNone(last_action)

    def test_cycle_until_negative_ends_with_signal(self):
        """Test cycle, ending on a node that returns a signal"""
        shared = {}
        n1 = NumberNode(10)           # post -> None
        check = CheckPositiveNode()   # post -> 'positive' or 'negative'
        subtract3 = AddNode(-3)       # post -> None
        end_node = EndSignalNode("cycle_done") # post -> "cycle_done"

        pipeline = Flow()
        pipeline.start(n1) >> check
        # Branching from CheckPositiveNode
        check - 'positive' >> subtract3
        check - 'negative' >> end_node # End on negative branch
        # After subtracting, go back to check (default transition)
        subtract3 >> check

        # Execution: n1->check->sub3->check->sub3->check->sub3->check->sub3->check->end_node
        last_action = pipeline.run(shared=shared)
        self.assertEqual(shared['current'], -2) # 10 -> 7 -> 4 -> 1 -> -2
        # Last node executed was end_node, its post returns "cycle_done"
        self.assertEqual(last_action, "cycle_done")

    def test_flow_ends_warning_default_missing(self):
        """Test warning when default transition is needed but not found"""
        shared = {}
        # Node that returns a specific action from post
        class ActionNode(Node):
            def post(self, shared, prep_res, exec_res): return "specific_action"
        start_node = ActionNode()
        next_node = NoOpNode()

        pipeline = Flow()
        pipeline.start(start_node)
        # Define successor only for the specific action
        start_node - "specific_action" >> next_node

        # Make start_node return None instead, triggering default search
        start_node.post = lambda shared, prep_res, exec_res: None

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Run flow. start_node runs, post returns None.
            # Flow looks for "default", but only "specific_action" exists.
            last_action = pipeline.run(shared=shared)

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            # Warning message should indicate "default" wasn't found
            self.assertIn("Flow ends: 'None' not found in ['specific_action']", str(w[-1].message))
        # Last action is from start_node's post
        self.assertIsNone(last_action)

    def test_flow_ends_warning_specific_missing(self):
        """Test warning when specific action is returned but not found"""
        shared = {}
        # Node that returns a specific action from post
        class ActionNode(Node):
            def post(self, *args, **kwargs): return "specific_action"
        start_node = ActionNode()
        next_node = NoOpNode()

        pipeline = Flow()
        pipeline.start(start_node)
        # Define successor only for "default"
        start_node >> next_node # same as start_node.next(next_node, "default")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Run flow. start_node runs, post returns "specific_action".
            # Flow looks for "specific_action", but only "default" exists.
            last_action = pipeline.run(shared)

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            # Warning message should indicate "specific_action" wasn't found
            self.assertIn("Flow ends: 'specific_action' not found in ['default']", str(w[-1].message))
        # Last action is from start_node's post
        self.assertEqual(last_action, "specific_action")


if __name__ == '__main__':
    unittest.main()