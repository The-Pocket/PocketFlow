import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import AsyncNode, AsyncBatchFlow

class AsyncDataProcessNode(AsyncNode):
    async def prep_async(self, shared_storage):
        key = self.params.get('key')
        data = shared_storage['input_data'][key]
        if 'results' not in shared_storage:
            shared_storage['results'] = {}
        shared_storage['results'][key] = data
        return data

    async def post_async(self, shared_storage, prep_result, proc_result):
        await asyncio.sleep(0.01)  # Simulate async work
        key = self.params.get('key')
        shared_storage['results'][key] = prep_result * 2  # Double the value
        return "processed"

class AsyncErrorNode(AsyncNode):
    async def post_async(self, shared_storage, prep_result, proc_result):
        key = self.params.get('key')
        if key == 'error_key':
            raise ValueError(f"Async error processing key: {key}")
        return "processed"

class TestAsyncBatchFlow(unittest.TestCase):
    def setUp(self):
        self.process_node = AsyncDataProcessNode()

    def test_basic_async_batch_processing(self):
        """Test basic async batch processing with multiple keys"""
        class SimpleTestAsyncBatchFlow(AsyncBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'key': k} for k in shared_storage['input_data'].keys()]

        shared_storage = {
            'input_data': {
                'a': 1,
                'b': 2,
                'c': 3
            }
        }

        flow = SimpleTestAsyncBatchFlow(start=self.process_node)
        asyncio.run(flow.run_async(shared_storage))

        expected_results = {
            'a': 2,  # 1 * 2
            'b': 4,  # 2 * 2
            'c': 6   # 3 * 2
        }
        self.assertEqual(shared_storage['results'], expected_results)

    def test_empty_async_batch(self):
        """Test async batch processing with empty input"""
        class EmptyTestAsyncBatchFlow(AsyncBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'key': k} for k in shared_storage['input_data'].keys()]

        shared_storage = {
            'input_data': {}
        }

        flow = EmptyTestAsyncBatchFlow(start=self.process_node)
        asyncio.run(flow.run_async(shared_storage))

        self.assertEqual(shared_storage.get('results', {}), {})

    def test_async_error_handling(self):
        """Test error handling during async batch processing"""
        class ErrorTestAsyncBatchFlow(AsyncBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'key': k} for k in shared_storage['input_data'].keys()]

        shared_storage = {
            'input_data': {
                'normal_key': 1,
                'error_key': 2,
                'another_key': 3
            }
        }

        flow = ErrorTestAsyncBatchFlow(start=AsyncErrorNode())
        
        with self.assertRaises(ValueError):
            asyncio.run(flow.run_async(shared_storage))

    def test_nested_async_flow(self):
        """Test async batch processing with nested flows"""
        class AsyncInnerNode(AsyncNode):
            async def post_async(self, shared_storage, prep_result, proc_result):
                key = self.params.get('key')
                if 'intermediate_results' not in shared_storage:
                    shared_storage['intermediate_results'] = {}
                shared_storage['intermediate_results'][key] = shared_storage['input_data'][key] + 1
                await asyncio.sleep(0.01)
                return "next"

        class AsyncOuterNode(AsyncNode):
            async def post_async(self, shared_storage, prep_result, proc_result):
                key = self.params.get('key')
                if 'results' not in shared_storage:
                    shared_storage['results'] = {}
                shared_storage['results'][key] = shared_storage['intermediate_results'][key] * 2
                await asyncio.sleep(0.01)
                return "done"

        class NestedAsyncBatchFlow(AsyncBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'key': k} for k in shared_storage['input_data'].keys()]

        # Create inner flow
        inner_node = AsyncInnerNode()
        outer_node = AsyncOuterNode()
        inner_node - "next" >> outer_node

        shared_storage = {
            'input_data': {
                'x': 1,
                'y': 2
            }
        }

        flow = NestedAsyncBatchFlow(start=inner_node)
        asyncio.run(flow.run_async(shared_storage))

        expected_results = {
            'x': 4,  # (1 + 1) * 2
            'y': 6   # (2 + 1) * 2
        }
        self.assertEqual(shared_storage['results'], expected_results)

    def test_custom_async_parameters(self):
        """Test async batch processing with additional custom parameters"""
        class CustomParamAsyncNode(AsyncNode):
            async def post_async(self, shared_storage, prep_result, proc_result):
                key = self.params.get('key')
                multiplier = self.params.get('multiplier', 1)
                await asyncio.sleep(0.01)
                if 'results' not in shared_storage:
                    shared_storage['results'] = {}
                shared_storage['results'][key] = shared_storage['input_data'][key] * multiplier
                return "done"

        class CustomParamAsyncBatchFlow(AsyncBatchFlow):
            async def prep_async(self, shared_storage):
                return [{
                    'key': k,
                    'multiplier': i + 1
                } for i, k in enumerate(shared_storage['input_data'].keys())]

        shared_storage = {
            'input_data': {
                'a': 1,
                'b': 2,
                'c': 3
            }
        }

        flow = CustomParamAsyncBatchFlow(start=CustomParamAsyncNode())
        asyncio.run(flow.run_async(shared_storage))

        expected_results = {
            'a': 1 * 1,  # first item, multiplier = 1
            'b': 2 * 2,  # second item, multiplier = 2
            'c': 3 * 3   # third item, multiplier = 3
        }
        self.assertEqual(shared_storage['results'], expected_results)

if __name__ == '__main__':
    unittest.main()