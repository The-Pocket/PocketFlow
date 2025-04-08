import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import AsyncNode, AsyncParallelBatchNode, AsyncParallelBatchFlow

class AsyncParallelNumberProcessor(AsyncParallelBatchNode):
    def __init__(self, delay=0.1):
        super().__init__()
        self.delay = delay
    
    async def prep_async(self, shared_storage):
        batch = shared_storage['batches'][self.params['batch_id']]
        return batch
    
    async def exec_async(self, number):
        await asyncio.sleep(self.delay)  # Simulate async processing
        return number * 2
        
    async def post_async(self, shared_storage, prep_result, exec_result):
        if 'processed_numbers' not in shared_storage:
            shared_storage['processed_numbers'] = {}
        shared_storage['processed_numbers'][self.params['batch_id']] = exec_result
        return "processed"

class AsyncAggregatorNode(AsyncNode):
    async def prep_async(self, shared_storage):
        # Combine all batch results in order
        all_results = []
        processed = shared_storage.get('processed_numbers', {})
        for i in range(len(processed)):
            all_results.extend(processed[i])
        return all_results
    
    async def exec_async(self, prep_result):
        await asyncio.sleep(0.01)
        return sum(prep_result)
    
    async def post_async(self, shared_storage, prep_result, exec_result):
        shared_storage['total'] = exec_result
        return "aggregated"

class TestAsyncParallelBatchFlow(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        self.loop.close()

    def test_parallel_batch_flow(self):
        """
        Test basic parallel batch processing flow with batch IDs
        """
        class TestParallelBatchFlow(AsyncParallelBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'batch_id': i} for i in range(len(shared_storage['batches']))]

        shared_storage = {
            'batches': [
                [1, 2, 3],  # batch_id: 0
                [4, 5, 6],  # batch_id: 1
                [7, 8, 9]   # batch_id: 2
            ]
        }

        processor = AsyncParallelNumberProcessor(delay=0.1)
        aggregator = AsyncAggregatorNode()
        
        processor - "processed" >> aggregator
        flow = TestParallelBatchFlow(start=processor)
        
        start_time = self.loop.time()
        self.loop.run_until_complete(flow.run_async(shared_storage))
        execution_time = self.loop.time() - start_time

        # Verify each batch was processed correctly
        expected_batch_results = {
            0: [2, 4, 6],    # [1,2,3] * 2
            1: [8, 10, 12],  # [4,5,6] * 2
            2: [14, 16, 18]  # [7,8,9] * 2
        }
        self.assertEqual(shared_storage['processed_numbers'], expected_batch_results)
        
        # Verify total
        expected_total = sum(num * 2 for batch in shared_storage['batches'] for num in batch)
        self.assertEqual(shared_storage['total'], expected_total)
        
        # Verify parallel execution
        self.assertLess(execution_time, 0.2)

    def test_error_handling(self):
        """
        Test error handling in parallel batch flow
        """
        class ErrorProcessor(AsyncParallelNumberProcessor):
            async def exec_async(self, item):
                if item == 2:
                    raise ValueError(f"Error processing item {item}")
                return item

        class ErrorBatchFlow(AsyncParallelBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'batch_id': i} for i in range(len(shared_storage['batches']))]

        shared_storage = {
            'batches': [
                [1, 2, 3],  # Contains error-triggering value
                [4, 5, 6]
            ]
        }

        processor = ErrorProcessor()
        flow = ErrorBatchFlow(start=processor)
        
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(flow.run_async(shared_storage))

    def test_multiple_batch_sizes(self):
        """
        Test parallel batch flow with varying batch sizes
        """
        class VaryingBatchFlow(AsyncParallelBatchFlow):
            async def prep_async(self, shared_storage):
                return [{'batch_id': i} for i in range(len(shared_storage['batches']))]

        shared_storage = {
            'batches': [
                [1],           # batch_id: 0
                [2, 3, 4],    # batch_id: 1
                [5, 6],       # batch_id: 2
                [7, 8, 9, 10] # batch_id: 3
            ]
        }

        processor = AsyncParallelNumberProcessor(delay=0.05)
        aggregator = AsyncAggregatorNode()
        
        processor - "processed" >> aggregator
        flow = VaryingBatchFlow(start=processor)
        
        self.loop.run_until_complete(flow.run_async(shared_storage))
        
        # Verify each batch was processed correctly
        expected_batch_results = {
            0: [2],                 # [1] * 2
            1: [4, 6, 8],          # [2,3,4] * 2
            2: [10, 12],           # [5,6] * 2
            3: [14, 16, 18, 20]    # [7,8,9,10] * 2
        }
        self.assertEqual(shared_storage['processed_numbers'], expected_batch_results)
        
        # Verify total
        expected_total = sum(num * 2 for batch in shared_storage['batches'] for num in batch)
        self.assertEqual(shared_storage['total'], expected_total)

if __name__ == '__main__':
    unittest.main()