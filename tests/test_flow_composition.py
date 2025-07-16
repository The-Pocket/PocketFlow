# tests/test_flow_composition.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Flow, Node


# --- Existing Nodes ---
class NumberNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] = self.number
    # post implicitly returns None

class AddNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] += self.number
    # post implicitly returns None

class MultiplyNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def prep(self, shared):
        shared['current'] *= self.number
    # post implicitly returns None

# --- New Nodes for Action Propagation Test ---
class SignalNode(Node):
    """A node that returns a specific signal string from its post method."""
    def __init__(self, signal="default_signal"):
        super().__init__()
        self.signal = signal
    # No prep needed usually if just signaling
    def post(self, shared, prep_res, exec_res):
        # Store the signal in shared storage for verification
        shared['last_signal_emitted'] = self.signal
        return self.signal # Return the specific action string

class PathNode(Node):
    """A node to indicate which path was taken in the outer flow."""
    def __init__(self, path_id):
        super().__init__()
        self.path_id = path_id
    def prep(self, shared):
        shared['path_taken'] = self.path_id
    # post implicitly returns None

# --- Test Class ---
class TestFlowComposition(unittest.TestCase):

    # --- Existing Tests (Unchanged) ---
    def test_flow_as_node(self):
        """
        1) Create a Flow (f1) starting with NumberNode(5), then AddNode(10), then MultiplyNode(2).
        2) Create a second Flow (f2) whose start is f1.
        3) Create a wrapper Flow (f3) that contains f2 to ensure proper execution.
        Expected final result in shared['current']: (5 + 10) * 2 = 30.
        """
        shared = {}
        f1 = Flow(start=NumberNode(5))
        f1 >> AddNode(10) >> MultiplyNode(2)
        f2 = Flow(start=f1)
        f3 = Flow(start=f2)
        f3.run(shared)
        self.assertEqual(shared['current'], 30)

    def test_nested_flow(self):
        """
        Demonstrates nested flows with proper wrapping:
        inner_flow: NumberNode(5) -> AddNode(3)
        middle_flow: starts with inner_flow -> MultiplyNode(4)
        wrapper_flow: contains middle_flow to ensure proper execution
        Expected final result: (5 + 3) * 4 = 32.
        """
        shared = {}
        inner_flow = Flow(start=NumberNode(5))
        inner_flow >> AddNode(3)
        middle_flow = Flow(start=inner_flow)
        middle_flow >> MultiplyNode(4)
        wrapper_flow = Flow(start=middle_flow)
        wrapper_flow.run(shared)
        self.assertEqual(shared['current'], 32)

    def test_flow_chaining_flows(self):
        """
        Demonstrates chaining two flows with proper wrapping:
        flow1: NumberNode(10) -> AddNode(10) # final = 20
        flow2: MultiplyNode(2) # final = 40
        wrapper_flow: contains both flow1 and flow2 to ensure proper execution
        Expected final result: (10 + 10) * 2 = 40.
        """
        shared = {}
        numbernode = NumberNode(10)
        numbernode >> AddNode(10)
        flow1 = Flow(start=numbernode)
        flow2 = Flow(start=MultiplyNode(2))
        flow1 >> flow2 # Default transition based on flow1 returning None
        wrapper_flow = Flow(start=flow1)
        wrapper_flow.run(shared)
        self.assertEqual(shared['current'], 40)

    def test_composition_with_action_propagation(self):
        """
        Test that an outer flow can branch based on the action returned
        by the last node's post() within an inner flow.
        """
        shared = {}

        # 1. Define an inner flow that ends with a node returning a specific action
        inner_start_node = NumberNode(100)       # current = 100, post -> None
        inner_end_node = SignalNode("inner_done") # post -> "inner_done"
        inner_start_node >> inner_end_node
        # Inner flow will execute start->end, and the Flow's execution will return "inner_done"
        inner_flow = Flow(start=inner_start_node)

        # 2. Define target nodes for the outer flow branches
        path_a_node = PathNode("A") # post -> None
        path_b_node = PathNode("B") # post -> None

        # 3. Define the outer flow starting with the inner flow
        outer_flow = Flow()
        outer_flow.start(inner_flow) # Use the start() method

        # 4. Define branches FROM the inner_flow object based on its returned action
        inner_flow - "inner_done" >> path_b_node  # This path should be taken
        inner_flow - "other_action" >> path_a_node # This path should NOT be taken

        # 5. Run the outer flow and capture the last action
        # Execution: inner_start -> inner_end -> path_b
        last_action_outer = outer_flow.run(shared)

        # 6. Assert the results
        # Check state after inner flow execution
        self.assertEqual(shared.get('current'), 100)
        self.assertEqual(shared.get('last_signal_emitted'), "inner_done")
        # Check that the correct outer path was taken
        self.assertEqual(shared.get('path_taken'), "B")
        # Check the action returned by the outer flow. The last node executed was
        # path_b_node, which returns None from its post method.
        self.assertIsNone(last_action_outer)

if __name__ == '__main__':
    unittest.main()