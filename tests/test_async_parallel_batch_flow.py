import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import AsyncFlow, AsyncNode, AsyncParallelBatchNode, AsyncParallelBatchFlow

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
        
        batch_flow = TestParallelBatchFlow(start=processor)
        batch_flow >> aggregator
        flow = AsyncFlow(start=batch_flow)
        
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

    def test_aggregation_waits_for_all_batches(self):
        async def run_test():
            all_started = asyncio.Event()
            release = [asyncio.Event() for _ in range(3)]
            release[2].set()

            class ControlledProcessor(AsyncParallelNumberProcessor):
                async def prep_async(self, shared_storage):
                    batch_id = self.params['batch_id']
                    shared_storage['started'].append(batch_id)
                    if len(shared_storage['started']) == 3:
                        all_started.set()
                    await all_started.wait()
                    await release[batch_id].wait()
                    return await super().prep_async(shared_storage)

                async def post_async(self, shared_storage, prep_result, exec_result):
                    action = await super().post_async(shared_storage, prep_result, exec_result)
                    batch_id = self.params['batch_id']
                    shared_storage['completed'].append(batch_id)
                    if batch_id > 0:
                        release[batch_id - 1].set()
                    return action

            class RecordingAggregator(AsyncAggregatorNode):
                async def prep_async(self, shared_storage):
                    shared_storage['aggregation_inputs'].append(
                        set(shared_storage['processed_numbers'])
                    )
                    return await super().prep_async(shared_storage)

            class ControlledBatchFlow(AsyncParallelBatchFlow):
                async def prep_async(self, shared_storage):
                    return [{'batch_id': i} for i in range(len(shared_storage['batches']))]

            shared_storage = {
                'batches': [[1, 2], [3], [4, 5, 6]],
                'started': [],
                'completed': [],
                'aggregation_inputs': [],
            }
            processor = ControlledProcessor(delay=0)
            aggregator = RecordingAggregator()
            batch_flow = ControlledBatchFlow(start=processor)
            batch_flow >> aggregator
            flow = AsyncFlow(start=batch_flow)

            # Bound the wait if batch execution accidentally becomes sequential.
            await asyncio.wait_for(flow.run_async(shared_storage), timeout=1)

            self.assertCountEqual(shared_storage['started'], [0, 1, 2])
            self.assertEqual(shared_storage['completed'], [2, 1, 0])
            self.assertEqual(shared_storage['aggregation_inputs'], [{0, 1, 2}])
            self.assertEqual(shared_storage['processed_numbers'], {
                0: [2, 4], 1: [6], 2: [8, 10, 12],
            })
            self.assertEqual(shared_storage['total'], 42)

        asyncio.run(run_test())

    def test_failed_batch_skips_aggregation(self):
        async def run_test():
            all_started = asyncio.Event()
            first_completed = asyncio.Event()
            release_error = asyncio.Event()
            release_survivor = asyncio.Event()
            branch_tasks = []
            error = ValueError("batch failed")
            shared = {'completed': [], 'aggregations': []}

            class ControlledProcessor(AsyncNode):
                async def prep_async(self, shared):
                    branch_tasks.append(asyncio.current_task())
                    if len(branch_tasks) == 3:
                        all_started.set()
                    await all_started.wait()
                    return self.params['batch_id']

                async def exec_async(self, batch_id):
                    if batch_id == 1:
                        await release_error.wait()
                        raise error
                    if batch_id == 2:
                        await release_survivor.wait()
                    return batch_id

                async def post_async(self, shared, prep_res, exec_res):
                    shared['completed'].append(exec_res)
                    first_completed.set()

            class RecordingAggregator(AsyncNode):
                async def prep_async(self, shared):
                    shared['aggregations'].append(list(shared['completed']))

            class ControlledBatchFlow(AsyncParallelBatchFlow):
                async def prep_async(self, shared):
                    return [{'batch_id': i} for i in range(3)]

            processor = ControlledProcessor()
            aggregator = RecordingAggregator()
            batch_flow = ControlledBatchFlow(start=processor)
            batch_flow >> aggregator
            flow = AsyncFlow(start=batch_flow)
            task = asyncio.create_task(flow.run_async(shared))
            try:
                await asyncio.wait_for(first_completed.wait(), timeout=1)
                self.assertEqual(shared['completed'], [0])
                self.assertEqual(shared['aggregations'], [])
                release_error.set()
                with self.assertRaises(ValueError) as caught:
                    await asyncio.wait_for(task, timeout=1)
                self.assertIs(caught.exception, error)
                self.assertEqual(shared['aggregations'], [])
                release_survivor.set()
                await asyncio.wait_for(
                    asyncio.gather(*branch_tasks, return_exceptions=True), timeout=1
                )
                self.assertEqual(shared['completed'], [0, 2])
                self.assertEqual(shared['aggregations'], [])
            finally:
                # A failed gather does not cancel siblings; own all test tasks.
                release_error.set()
                release_survivor.set()
                if not task.done():
                    task.cancel()
                await asyncio.gather(task, *branch_tasks, return_exceptions=True)

        asyncio.run(run_test())

    def test_cancelled_batch_skips_aggregation(self):
        async def run_test():
            all_started = asyncio.Event()
            first_completed = asyncio.Event()
            release = asyncio.Event()
            branch_tasks = []
            finished = []
            cancelled = []
            shared = {'completed': [], 'aggregations': []}

            class ControlledProcessor(AsyncNode):
                async def prep_async(self, shared):
                    batch_id = self.params['batch_id']
                    branch_tasks.append(asyncio.current_task())
                    if len(branch_tasks) == 3:
                        all_started.set()
                    try:
                        await all_started.wait()
                        if batch_id != 0:
                            await release.wait()
                        return batch_id
                    except asyncio.CancelledError:
                        cancelled.append(batch_id)
                        raise
                    finally:
                        finished.append(batch_id)

                async def post_async(self, shared, prep_res, exec_res):
                    shared['completed'].append(prep_res)
                    first_completed.set()

            class RecordingAggregator(AsyncNode):
                async def prep_async(self, shared):
                    shared['aggregations'].append(list(shared['completed']))

            class ControlledBatchFlow(AsyncParallelBatchFlow):
                async def prep_async(self, shared):
                    return [{'batch_id': i} for i in range(3)]

            processor = ControlledProcessor()
            aggregator = RecordingAggregator()
            batch_flow = ControlledBatchFlow(start=processor)
            batch_flow >> aggregator
            flow = AsyncFlow(start=batch_flow)
            task = asyncio.create_task(flow.run_async(shared))
            try:
                await asyncio.wait_for(first_completed.wait(), timeout=1)
                self.assertEqual(shared['completed'], [0])
                self.assertEqual(shared['aggregations'], [])
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, timeout=1)
                self.assertTrue(task.cancelled())
                self.assertCountEqual(cancelled, [1, 2])
                self.assertCountEqual(finished, [0, 1, 2])
                self.assertEqual(shared['aggregations'], [])
            finally:
                release.set()
                if not task.done():
                    task.cancel()
                await asyncio.gather(task, *branch_tasks, return_exceptions=True)

        asyncio.run(run_test())

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
        
        batch_flow = VaryingBatchFlow(start=processor)
        batch_flow >> aggregator
        flow = AsyncFlow(start=batch_flow)
        
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

class AsyncItemNode(AsyncNode):
    async def prep_async(self, shared_storage):
        return shared_storage['groups'][self.params['group']][self.params['item']]
    async def exec_async(self, prep_res):
        return prep_res * 2
    async def post_async(self, shared_storage, prep_res, exec_res):
        group = self.params['group']
        if 'results' not in shared_storage:
            shared_storage['results'] = {}
        if group not in shared_storage['results']:
            shared_storage['results'][group] = []
        shared_storage['results'][group].append(exec_res)

class InnerAsyncParallelBatchFlow(AsyncParallelBatchFlow):
    async def prep_async(self, shared_storage):
        group = self.params['group']
        return [{'item': i, 'group': group} for i in range(len(shared_storage['groups'][group]))]

class OuterAsyncParallelBatchFlow(AsyncParallelBatchFlow):
    async def prep_async(self, shared_storage):
        return [{'group': g} for g in shared_storage['groups']]

class TestNestedAsyncParallelBatchFlow(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_nested_parallel_batch_flow(self):
        """Test AsyncParallelBatchFlow nested inside another (same structure as sync test)"""
        item_node = AsyncItemNode()
        inner_flow = InnerAsyncParallelBatchFlow(start=item_node)
        outer_flow = OuterAsyncParallelBatchFlow(start=inner_flow)

        shared_storage = {
            'groups': {
                'A': [1, 2],
                'B': [3, 4],
            }
        }

        self.loop.run_until_complete(outer_flow.run_async(shared_storage))

        expected = {
            'A': [2, 4],
            'B': [6, 8],
        }
        self.assertEqual(sorted(shared_storage['results'].keys()), sorted(expected.keys()))
        for group in expected:
            self.assertCountEqual(shared_storage['results'][group], expected[group])

if __name__ == '__main__':
    unittest.main()