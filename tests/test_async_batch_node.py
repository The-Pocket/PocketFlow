import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import AsyncNode, AsyncBatchNode, AsyncFlow

class AsyncArrayChunkNode(AsyncBatchNode):
    def __init__(self, chunk_size=10):
        super().__init__()
        self.chunk_size = chunk_size
    
    async def prep_async(self, shared_storage):
        # Get array from shared storage and split into chunks
        array = shared_storage.get('input_array', [])
        chunks = []
        for start in range(0, len(array), self.chunk_size):
            end = min(start + self.chunk_size, len(array))
            chunks.append(array[start:end])
        return chunks
    
    async def exec_async(self, chunk):
        # Simulate async processing of each chunk
        await asyncio.sleep(0.01)
        return sum(chunk)
        
    async def post_async(self, shared_storage, prep_result, proc_result):
        # Store chunk results in shared storage
        shared_storage['chunk_results'] = proc_result
        return "processed"

class AsyncSumReduceNode(AsyncNode):
    async def prep_async(self, shared_storage):
        # Get chunk results from shared storage
        chunk_results = shared_storage.get('chunk_results', [])
        await asyncio.sleep(0.01)  # Simulate async processing
        total = sum(chunk_results)
        shared_storage['total'] = total
        return "reduced"

class TestAsyncBatchNode(unittest.TestCase):
    def test_array_chunking(self):
        """
        Test that the array is correctly split into chunks and processed asynchronously
        """
        shared_storage = {
            'input_array': list(range(25))  # [0,1,2,...,24]
        }
        
        chunk_node = AsyncArrayChunkNode(chunk_size=10)
        asyncio.run(chunk_node.run_async(shared_storage))
        
        results = shared_storage['chunk_results']
        self.assertEqual(results, [45, 145, 110])  # Sum of chunks [0-9], [10-19], [20-24]
        
    # def test_async_map_reduce_sum(self):
    #     """
    #     Test a complete async map-reduce pipeline that sums a large array:
    #     1. Map: Split array into chunks and sum each chunk asynchronously
    #     2. Reduce: Sum all the chunk sums asynchronously
    #     """
    #     array = list(range(100))
    #     expected_sum = sum(array)  # 4950
        
    #     shared_storage = {
    #         'input_array': array
    #     }
        
    #     # Create nodes
    #     chunk_node = AsyncArrayChunkNode(chunk_size=10)
    #     reduce_node = AsyncSumReduceNode()
        
    #     # Connect nodes
    #     chunk_node - "processed" >> reduce_node
        
    #     # Create and run pipeline
    #     pipeline = AsyncFlow(start=chunk_node)
    #     asyncio.run(pipeline.run_async(shared_storage))
        
    #     self.assertEqual(shared_storage['total'], expected_sum)
        
    # def test_uneven_chunks(self):
    #     """
    #     Test that the async map-reduce works correctly with array lengths
    #     that don't divide evenly by chunk_size
    #     """
    #     array = list(range(25))
    #     expected_sum = sum(array)  # 300
        
    #     shared_storage = {
    #         'input_array': array
    #     }
        
    #     chunk_node = AsyncArrayChunkNode(chunk_size=10)
    #     reduce_node = AsyncSumReduceNode()
        
    #     chunk_node - "processed" >> reduce_node
    #     pipeline = AsyncFlow(start=chunk_node)
    #     asyncio.run(pipeline.run_async(shared_storage))
        
    #     self.assertEqual(shared_storage['total'], expected_sum)

    # def test_custom_chunk_size(self):
    #     """
    #     Test that the async map-reduce works with different chunk sizes
    #     """
    #     array = list(range(100))
    #     expected_sum = sum(array)
        
    #     shared_storage = {
    #         'input_array': array
    #     }
        
    #     # Use chunk_size=15 instead of default 10
    #     chunk_node = AsyncArrayChunkNode(chunk_size=15)
    #     reduce_node = AsyncSumReduceNode()
        
    #     chunk_node - "processed" >> reduce_node
    #     pipeline = AsyncFlow(start=chunk_node)
    #     asyncio.run(pipeline.run_async(shared_storage))
        
    #     self.assertEqual(shared_storage['total'], expected_sum)
        
    # def test_single_element_chunks(self):
    #     """
    #     Test extreme case where chunk_size=1
    #     """
    #     array = list(range(5))
    #     expected_sum = sum(array)
        
    #     shared_storage = {
    #         'input_array': array
    #     }
        
    #     chunk_node = AsyncArrayChunkNode(chunk_size=1)
    #     reduce_node = AsyncSumReduceNode()
        
    #     chunk_node - "processed" >> reduce_node
    #     pipeline = AsyncFlow(start=chunk_node)
    #     asyncio.run(pipeline.run_async(shared_storage))
        
    #     self.assertEqual(shared_storage['total'], expected_sum)

    # def test_empty_array(self):
    #     """
    #     Test edge case of empty input array
    #     """
    #     shared_storage = {
    #         'input_array': []
    #     }
        
    #     chunk_node = AsyncArrayChunkNode(chunk_size=10)
    #     reduce_node = AsyncSumReduceNode()
        
    #     chunk_node - "processed" >> reduce_node
    #     pipeline = AsyncFlow(start=chunk_node)
    #     asyncio.run(pipeline.run_async(shared_storage))
        
    #     self.assertEqual(shared_storage['total'], 0)

    # def test_error_handling(self):
    #     """
    #     Test error handling in async batch processing
    #     """
    #     class ErrorAsyncBatchNode(AsyncBatchNode):
    #         async def exec_async(self, item):
    #             if item == 2:
    #                 raise ValueError("Error processing item 2")
    #             return item

    #     shared_storage = {
    #         'input_array': [1, 2, 3]
    #     }
        
    #     error_node = ErrorAsyncBatchNode()
    #     with self.assertRaises(ValueError):
    #         asyncio.run(error_node.run_async(shared_storage))

if __name__ == '__main__':
    unittest.main()