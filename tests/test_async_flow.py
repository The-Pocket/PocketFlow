import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Node, AsyncNode, AsyncFlow


class AsyncNumberNode(AsyncNode):
    """
    Simple async node that sets 'current' to a given number.
    Demonstrates overriding .process() (sync) and using
    post_async() for the async portion.
    """
    def __init__(self, number):
        super().__init__()
        self.number = number

    async def prep_async(self, shared_storage):
        # Synchronous work is allowed inside an AsyncNode,
        # but final 'condition' is determined by post_async().
        shared_storage['current'] = self.number
        return "set_number"

    async def post_async(self, shared_storage, prep_result, proc_result):
        # Possibly do asynchronous tasks here
        await asyncio.sleep(0.01)
        # Return a condition for the flow
        return "number_set"


class AsyncIncrementNode(AsyncNode):
    """
    Demonstrates incrementing the 'current' value asynchronously.
    """
    async def prep_async(self, shared_storage):
        shared_storage['current'] = shared_storage.get('current', 0) + 1
        return "incremented"

    async def post_async(self, shared_storage, prep_result, proc_result):
        await asyncio.sleep(0.01)  # simulate async I/O
        return "done"


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
            shared_storage = {}
            condition = await node.run_async(shared_storage)
            return shared_storage, condition

        shared_storage, condition = asyncio.run(run_node())
        self.assertEqual(shared_storage['current'], 42)
        self.assertEqual(condition, "number_set")

    def test_async_increment_node_direct_call(self):
        async def run_node():
            node = AsyncIncrementNode()
            shared_storage = {'current': 10}
            condition = await node.run_async(shared_storage)
            return shared_storage, condition

        shared_storage, condition = asyncio.run(run_node())
        self.assertEqual(shared_storage['current'], 11)
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
        shared_storage = {}
        asyncio.run(flow.run_async(shared_storage))

        self.assertEqual(shared_storage['current'], 6)

    def test_async_flow_branching(self):
        """
        Demonstrate a branching scenario where we return different
        conditions. For example, you could have an async node that
        returns "go_left" or "go_right" in post_async, but here
        we'll keep it simpler for demonstration.
        """

        class BranchingAsyncNode(AsyncNode):
            def exec(self, data):
                value = shared_storage.get("value", 0)
                shared_storage["value"] = value
                # We'll decide branch based on whether 'value' is positive
                return None

            async def post_async(self, shared_storage, prep_result, proc_result):
                await asyncio.sleep(0.01)
                if shared_storage["value"] >= 0:
                    return "positive_branch"
                else:
                    return "negative_branch"

        class PositiveNode(Node):
            def exec(self, data):
                shared_storage["path"] = "positive"
                return None

        class NegativeNode(Node):
            def exec(self, data):
                shared_storage["path"] = "negative"
                return None

        shared_storage = {"value": 10}

        start = BranchingAsyncNode()
        positive_node = PositiveNode()
        negative_node = NegativeNode()

        # Condition-based chaining
        start - "positive_branch" >> positive_node
        start - "negative_branch" >> negative_node

        flow = AsyncFlow(start)
        asyncio.run(flow.run_async(shared_storage))

        self.assertEqual(shared_storage["path"], "positive", 
                         "Should have taken the positive branch")


if __name__ == '__main__':
    unittest.main()
