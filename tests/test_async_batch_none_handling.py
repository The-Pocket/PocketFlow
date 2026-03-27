"""Tests for AsyncBatchNode/AsyncParallelBatchNode handling of None prep results."""

import unittest
import asyncio
from pocketflow import AsyncBatchNode, AsyncParallelBatchNode, BatchNode


class TestBatchNodeNoneHandling(unittest.TestCase):
    """Verify synchronous BatchNode handles None gracefully (baseline)."""

    def test_batch_node_none_returns_empty(self):
        """BatchNode with None prep result should return []."""

        class MyBatch(BatchNode):
            def exec(self, prep_res):
                return f"processed:{prep_res}"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        node = MyBatch()
        # prep returns None by default, _exec gets None
        result = node._run({})
        self.assertEqual(result, [])

    def test_batch_node_empty_list_returns_empty(self):
        """BatchNode with empty list should return []."""

        class MyBatch(BatchNode):
            def prep(self, shared):
                return shared.get("items", [])

            def exec(self, prep_res):
                return f"processed:{prep_res}"

            def post(self, shared, prep_res, exec_res):
                return exec_res

        node = MyBatch()
        result = node.run({"items": []})
        self.assertEqual(result, [])


class TestAsyncBatchNodeNoneHandling(unittest.TestCase):
    """AsyncBatchNode must handle None prep results like BatchNode does."""

    def test_async_batch_node_none_returns_empty(self):
        """AsyncBatchNode with None prep result should return [], not crash."""

        class MyAsyncBatch(AsyncBatchNode):
            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncBatch()
        result = asyncio.run(node._run_async({}))
        self.assertEqual(result, [])

    def test_async_batch_node_empty_list_returns_empty(self):
        """AsyncBatchNode with empty list should return []."""

        class MyAsyncBatch(AsyncBatchNode):
            async def prep_async(self, shared):
                return shared.get("items", [])

            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncBatch()
        result = asyncio.run(node.run_async({"items": []}))
        self.assertEqual(result, [])

    def test_async_batch_node_with_data(self):
        """AsyncBatchNode should still work correctly with actual data."""

        class MyAsyncBatch(AsyncBatchNode):
            async def prep_async(self, shared):
                return shared.get("items", [])

            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncBatch()
        result = asyncio.run(node.run_async({"items": ["a", "b", "c"]}))
        self.assertEqual(result, ["processed:a", "processed:b", "processed:c"])


class TestAsyncParallelBatchNodeNoneHandling(unittest.TestCase):
    """AsyncParallelBatchNode must handle None prep results like BatchNode does."""

    def test_async_parallel_batch_node_none_returns_empty(self):
        """AsyncParallelBatchNode with None prep result should return [], not crash."""

        class MyAsyncParallelBatch(AsyncParallelBatchNode):
            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncParallelBatch()
        result = asyncio.run(node._run_async({}))
        self.assertEqual(result, [])

    def test_async_parallel_batch_node_empty_list_returns_empty(self):
        """AsyncParallelBatchNode with empty list should return []."""

        class MyAsyncParallelBatch(AsyncParallelBatchNode):
            async def prep_async(self, shared):
                return shared.get("items", [])

            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncParallelBatch()
        result = asyncio.run(node.run_async({"items": []}))
        self.assertEqual(result, [])

    def test_async_parallel_batch_node_with_data(self):
        """AsyncParallelBatchNode should still work correctly with actual data."""

        class MyAsyncParallelBatch(AsyncParallelBatchNode):
            async def prep_async(self, shared):
                return shared.get("items", [])

            async def exec_async(self, prep_res):
                return f"processed:{prep_res}"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = MyAsyncParallelBatch()
        result = asyncio.run(node.run_async({"items": ["a", "b", "c"]}))
        # Parallel execution may reorder, so compare as sets
        self.assertEqual(set(result), {"processed:a", "processed:b", "processed:c"})


if __name__ == "__main__":
    unittest.main()
