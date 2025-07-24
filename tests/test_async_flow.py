import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import AsyncFlow, AsyncNode, Node


class AsyncNumberNode(AsyncNode):
    """
    Simple async node that sets 'current' to a given number.
    Demonstrates overriding .process() (sync) and using
    post_async() for the async portion.
    """
    def __init__(self, number):
        super().__init__()
        self.number = number

    async def prep_async(self, shared):
        # Synchronous work is allowed inside an AsyncNode,
        # but final 'condition' is determined by post_async().
        shared['current'] = self.number
        return "set_number"

    async def post_async(self, shared, prep_res, exec_res):
        # Possibly do asynchronous tasks here
        await asyncio.sleep(0.01)
        # Return a condition for the flow
        return "number_set"

class AsyncIncrementNode(AsyncNode):
    """
    Demonstrates incrementing the 'current' value asynchronously.
    """
    async def prep_async(self, shared):
        shared['current'] = shared.get('current', 0) + 1
        return "incremented"

    async def post_async(self, shared, prep_res, exec_res):
        await asyncio.sleep(0.01)  # simulate async I/O
        return "done"

class AsyncSignalNode(AsyncNode):
    """ An async node that returns a specific signal string from post_async. """
    def __init__(self, signal="default_async_signal"):
        super().__init__()
        self.signal = signal

    # No prep needed usually if just signaling
    async def prep_async(self, shared):
        await asyncio.sleep(0.01) # Simulate async work

    async def post_async(self, shared, prep_res, exec_res):
        # Store the signal in shared storage for verification
        shared['last_async_signal_emitted'] = self.signal
        await asyncio.sleep(0.01) # Simulate async work
        print(self.signal)
        return self.signal # Return the specific action string

class AsyncPathNode(AsyncNode):
    """ An async node to indicate which path was taken in the outer flow. """
    def __init__(self, path_id):
        super().__init__()
        self.path_id = path_id

    async def prep_async(self, shared):
        await asyncio.sleep(0.01) # Simulate async work
        shared['async_path_taken'] = self.path_id

    # post_async implicitly returns None (for default transition out if needed)
    async def post_async(self, shared, prep_res, exec_res):
         await asyncio.sleep(0.01)
         # Return None by default

class TestAsyncNode(unittest.TestCase):
    """
    Test the AsyncNode (and descendants) in isolation (not in a flow).
    """
    def test_async_number_node_direct_call(self):
        """
        Even though AsyncNumberNode is designed for an async flow,
        we can still test it directly by calling run_async().
        """
        async def run_node():
            node = AsyncNumberNode(42)
            shared = {}
            condition = await node.run_async(shared)
            return shared, condition

        shared, condition = asyncio.run(run_node())
        self.assertEqual(shared['current'], 42)
        self.assertEqual(condition, "number_set")

    def test_async_increment_node_direct_call(self):
        async def run_node():
            node = AsyncIncrementNode()
            shared = {'current': 10}
            condition = await node.run_async(shared)
            return shared, condition

        shared, condition = asyncio.run(run_node())
        self.assertEqual(shared['current'], 11)
        self.assertEqual(condition, "done")


class TestAsyncFlow(unittest.TestCase):
    """
    Test how AsyncFlow orchestrates multiple async nodes.
    """
    def test_simple_async_flow(self):
        """
        Flow:
          1) AsyncNumberNode(5) -> sets 'current' to 5
          2) AsyncIncrementNode() -> increments 'current' to 6
        """

        # Create our nodes
        start = AsyncNumberNode(5)
        inc_node = AsyncIncrementNode()

        # Chain them: start >> inc_node
        start - "number_set" >> inc_node

        # Create an AsyncFlow with start
        flow = AsyncFlow(start)

        # We'll run the flow synchronously (which under the hood is asyncio.run())
        shared = {}
        asyncio.run(flow.run_async(shared))

        self.assertEqual(shared['current'], 6)

    def test_async_flow_branching(self):
        """
        Demonstrate a branching scenario where we return different
        conditions. For example, you could have an async node that
        returns "go_left" or "go_right" in post_async, but here
        we'll keep it simpler for demonstration.
        """

        class BranchingAsyncNode(AsyncNode):
            def exec(self, prep_res):
                value = shared.get("value", 0)
                shared["value"] = value
                # We'll decide branch based on whether 'value' is positive
                return None

            async def post_async(self, shared, prep_res, exec_res):
                await asyncio.sleep(0.01)
                if shared["value"] >= 0:
                    return "positive_branch"
                else:
                    return "negative_branch"

        class PositiveNode(Node):
            def exec(self, prep_res):
                shared["path"] = "positive"
                return None

        class NegativeNode(Node):
            def exec(self, prep_res):
                shared["path"] = "negative"
                return None

        shared = {"value": 10}

        start = BranchingAsyncNode()
        positive_node = PositiveNode()
        negative_node = NegativeNode()

        # Condition-based chaining
        start - "positive_branch" >> positive_node
        start - "negative_branch" >> negative_node

        flow = AsyncFlow(start)
        asyncio.run(flow.run_async(shared))

        self.assertEqual(shared["path"], "positive", 
                         "Should have taken the positive branch")

    def test_async_composition_with_action_propagation(self):
        """
        Test AsyncFlow branches based on action from nested AsyncFlow's last node.
        """
        async def run_test():
            shared = {}

            # 1. Define an inner async flow ending with AsyncSignalNode
            # Use existing AsyncNumberNode which should return None from post_async implicitly
            inner_start_node = AsyncNumberNode(200)
            inner_end_node = AsyncSignalNode("async_inner_done") # post_async -> "async_inner_done"
            inner_start_node - "number_set" >> inner_end_node
            # Inner flow will execute start->end, Flow exec returns "async_inner_done"
            inner_flow = AsyncFlow(start=inner_start_node)

            # 2. Define target async nodes for the outer flow branches
            path_a_node = AsyncPathNode("AsyncA") # post_async -> None
            path_b_node = AsyncPathNode("AsyncB") # post_async -> None

            # 3. Define the outer async flow starting with the inner async flow
            outer_flow = AsyncFlow(start=inner_flow)

            # 4. Define branches FROM the inner_flow object based on its returned action
            inner_flow - "async_inner_done" >> path_b_node  # This path should be taken
            inner_flow - "other_action" >> path_a_node      # This path should NOT be taken

            # 5. Run the outer async flow and capture the last action
            # Execution: inner_start -> inner_end -> path_b
            last_action_outer = await outer_flow.run_async(shared)

            # 6. Return results for assertion
            return shared, last_action_outer

        # Run the async test function
        shared, last_action_outer = asyncio.run(run_test())

        # 7. Assert the results
        # Check state after inner flow execution
        self.assertEqual(shared.get('current'), 200) # From AsyncNumberNode
        self.assertEqual(shared.get('last_async_signal_emitted'), "async_inner_done")
        # Check that the correct outer path was taken
        self.assertEqual(shared.get('async_path_taken'), "AsyncB")
        # Check the action returned by the outer flow. The last node executed was
        # path_b_node, which returns None from its post_async method.
        self.assertIsNone(last_action_outer)

if __name__ == '__main__':
    unittest.main()
