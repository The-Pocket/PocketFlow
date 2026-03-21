"""Tests for Node parameter validation (max_retries, wait)."""

import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketflow import Node, AsyncNode, Flow


class DummyNode(Node):
    """A simple node that always succeeds."""

    def exec(self, prep_res):
        return "ok"

    def post(self, shared, prep_res, exec_res):
        return exec_res


class TestMaxRetriesValidation(unittest.TestCase):
    """Test that max_retries rejects invalid values."""

    def test_max_retries_zero_raises(self):
        """max_retries=0 should raise ValueError, not silently skip execution."""
        with self.assertRaises(ValueError) as ctx:
            Node(max_retries=0)
        self.assertIn("max_retries", str(ctx.exception))

    def test_max_retries_negative_raises(self):
        """max_retries=-1 should raise ValueError."""
        with self.assertRaises(ValueError):
            Node(max_retries=-1)

    def test_max_retries_negative_large_raises(self):
        """Large negative max_retries should raise ValueError."""
        with self.assertRaises(ValueError):
            Node(max_retries=-100)

    def test_max_retries_one_succeeds(self):
        """max_retries=1 (default) should work normally."""
        node = DummyNode(max_retries=1)
        result = node.run({})
        self.assertEqual(result, "ok")

    def test_max_retries_positive_succeeds(self):
        """max_retries=3 should work normally."""
        node = DummyNode(max_retries=3)
        result = node.run({})
        self.assertEqual(result, "ok")

    def test_default_max_retries_is_one(self):
        """Default max_retries should be 1."""
        node = DummyNode()
        self.assertEqual(node.max_retries, 1)


class TestWaitValidation(unittest.TestCase):
    """Test that wait rejects negative values."""

    def test_wait_negative_raises(self):
        """wait=-1 should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            Node(wait=-1)
        self.assertIn("wait", str(ctx.exception))

    def test_wait_zero_succeeds(self):
        """wait=0 (default) should work normally."""
        node = DummyNode(wait=0)
        result = node.run({})
        self.assertEqual(result, "ok")

    def test_wait_positive_succeeds(self):
        """wait=0.1 should work normally."""
        node = DummyNode(max_retries=1, wait=0.1)
        result = node.run({})
        self.assertEqual(result, "ok")

    def test_default_wait_is_zero(self):
        """Default wait should be 0."""
        node = DummyNode()
        self.assertEqual(node.wait, 0)


class TestAsyncNodeValidation(unittest.TestCase):
    """Test that AsyncNode inherits the same validation."""

    def test_async_max_retries_zero_raises(self):
        """AsyncNode with max_retries=0 should raise ValueError."""
        with self.assertRaises(ValueError):
            AsyncNode(max_retries=0)

    def test_async_max_retries_negative_raises(self):
        """AsyncNode with max_retries=-1 should raise ValueError."""
        with self.assertRaises(ValueError):
            AsyncNode(max_retries=-1)

    def test_async_wait_negative_raises(self):
        """AsyncNode with wait=-1 should raise ValueError."""
        with self.assertRaises(ValueError):
            AsyncNode(wait=-1)

    def test_async_valid_params_succeeds(self):
        """AsyncNode with valid params should work normally."""

        class AsyncDummy(AsyncNode):
            async def exec_async(self, prep_res):
                return "ok"

            async def post_async(self, shared, prep_res, exec_res):
                return exec_res

        node = AsyncDummy(max_retries=2, wait=0.01)
        result = asyncio.run(node.run_async({}))
        self.assertEqual(result, "ok")


class TestNodeExecIsCalled(unittest.TestCase):
    """Verify that exec() is actually called with valid params."""

    def test_exec_called_with_max_retries_1(self):
        """exec() should be called exactly once with max_retries=1."""

        class CounterNode(Node):
            def __init__(self):
                super().__init__(max_retries=1)
                self.count = 0

            def exec(self, prep_res):
                self.count += 1
                return self.count

            def post(self, shared, prep_res, exec_res):
                return exec_res

        node = CounterNode()
        result = node.run({})
        self.assertEqual(result, 1)
        self.assertEqual(node.count, 1)

    def test_retry_calls_exec_multiple_times(self):
        """With max_retries=3 and always-fail, exec should be called 3 times."""

        class FailNode(Node):
            def __init__(self):
                super().__init__(max_retries=3)
                self.count = 0

            def exec(self, prep_res):
                self.count += 1
                raise RuntimeError(f"fail #{self.count}")

        node = FailNode()
        with self.assertRaises(RuntimeError) as ctx:
            node.run({})
        self.assertEqual(node.count, 3)
        self.assertIn("fail #3", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
