import unittest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Node, AsyncNode, Flow, AsyncFlow

class FallbackNode(Node):
    def __init__(self, should_fail=True, max_retries=1):
        super().__init__(max_retries=max_retries)
        self.should_fail = should_fail
        self.attempt_count = 0
    
    def prep(self, shared_storage):
        if 'results' not in shared_storage:
            shared_storage['results'] = []
        return None
    
    def exec(self, prep_result):
        self.attempt_count += 1
        if self.should_fail:
            raise ValueError("Intentional failure")
        return "success"
    
    def exec_fallback(self, prep_result, exc):
        return "fallback"
    
    def post(self, shared_storage, prep_result, exec_result):
        shared_storage['results'].append({
            'attempts': self.attempt_count,
            'result': exec_result
        })

class AsyncFallbackNode(AsyncNode):
    def __init__(self, should_fail=True, max_retries=1):
        super().__init__(max_retries=max_retries)
        self.should_fail = should_fail
        self.attempt_count = 0
    
    async def prep_async(self, shared_storage):
        if 'results' not in shared_storage:
            shared_storage['results'] = []
        return None
    
    async def exec_async(self, prep_result):
        self.attempt_count += 1
        if self.should_fail:
            raise ValueError("Intentional async failure")
        return "success"
    
    async def exec_fallback_async(self, prep_result, exc):
        await asyncio.sleep(0.01)  # Simulate async work
        return "async_fallback"
    
    async def post_async(self, shared_storage, prep_result, exec_result):
        shared_storage['results'].append({
            'attempts': self.attempt_count,
            'result': exec_result
        })

class TestExecFallback(unittest.TestCase):
    def test_successful_execution(self):
        """Test that exec_fallback is not called when execution succeeds"""
        shared_storage = {}
        node = FallbackNode(should_fail=False)
        result = node.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 1)
        self.assertEqual(shared_storage['results'][0]['result'], "success")

    def test_fallback_after_failure(self):
        """Test that exec_fallback is called after all retries are exhausted"""
        shared_storage = {}
        node = FallbackNode(should_fail=True, max_retries=2)
        result = node.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 2)
        self.assertEqual(shared_storage['results'][0]['result'], "fallback")

    def test_fallback_in_flow(self):
        """Test that fallback works within a Flow"""
        class ResultNode(Node):
            def prep(self, shared_storage):
                return shared_storage.get('results', [])
                
            def exec(self, prep_result):
                return prep_result
                
            def post(self, shared_storage, prep_result, exec_result):
                shared_storage['final_result'] = exec_result
                return None
        
        shared_storage = {}
        fallback_node = FallbackNode(should_fail=True)
        result_node = ResultNode()
        fallback_node >> result_node
        
        flow = Flow(start=fallback_node)
        flow.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['result'], "fallback")
        self.assertEqual(shared_storage['final_result'], [{'attempts': 1, 'result': 'fallback'}] )

    def test_no_fallback_implementation(self):
        """Test that default fallback behavior raises the exception"""
        class NoFallbackNode(Node):
            def prep(self, shared_storage):
                if 'results' not in shared_storage:
                    shared_storage['results'] = []
                return None
            
            def exec(self, prep_result):
                raise ValueError("Test error")
            
            def post(self, shared_storage, prep_result, exec_result):
                shared_storage['results'].append({'result': exec_result})
                return exec_result
        
        shared_storage = {}
        node = NoFallbackNode()
        with self.assertRaises(ValueError):
            node.run(shared_storage)

    def test_retry_before_fallback(self):
        """Test that retries are attempted before calling fallback"""
        shared_storage = {}
        node = FallbackNode(should_fail=True, max_retries=3)
        node.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 3)
        self.assertEqual(shared_storage['results'][0]['result'], "fallback")

class TestAsyncExecFallback(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        self.loop.close()

    def test_async_successful_execution(self):
        """Test that async exec_fallback is not called when execution succeeds"""
        async def run_test():
            shared_storage = {}
            node = AsyncFallbackNode(should_fail=False)
            await node.run_async(shared_storage)
            return shared_storage
        
        shared_storage = self.loop.run_until_complete(run_test())
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 1)
        self.assertEqual(shared_storage['results'][0]['result'], "success")

    def test_async_fallback_after_failure(self):
        """Test that async exec_fallback is called after all retries are exhausted"""
        async def run_test():
            shared_storage = {}
            node = AsyncFallbackNode(should_fail=True, max_retries=2)
            await node.run_async(shared_storage)
            return shared_storage
        
        shared_storage = self.loop.run_until_complete(run_test())
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 2)
        self.assertEqual(shared_storage['results'][0]['result'], "async_fallback")

    def test_async_fallback_in_flow(self):
        """Test that async fallback works within an AsyncFlow"""
        class AsyncResultNode(AsyncNode):
            async def prep_async(self, shared_storage):
                return shared_storage['results'][-1]['result']  # Get last result
                
            async def exec_async(self, prep_result):
                return prep_result
                
            async def post_async(self, shared_storage, prep_result, exec_result):
                shared_storage['final_result'] = exec_result
                return "done"
        
        async def run_test():
            shared_storage = {}
            fallback_node = AsyncFallbackNode(should_fail=True)
            result_node = AsyncResultNode()
            fallback_node >> result_node
            
            flow = AsyncFlow(start=fallback_node)
            await flow.run_async(shared_storage)
            return shared_storage
        
        shared_storage = self.loop.run_until_complete(run_test())
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['result'], "async_fallback")
        self.assertEqual(shared_storage['final_result'], "async_fallback")

    def test_async_no_fallback_implementation(self):
        """Test that default async fallback behavior raises the exception"""
        class NoFallbackAsyncNode(AsyncNode):
            async def prep_async(self, shared_storage):
                if 'results' not in shared_storage:
                    shared_storage['results'] = []
                return None
            
            async def exec_async(self, prep_result):
                raise ValueError("Test async error")
            
            async def post_async(self, shared_storage, prep_result, exec_result):
                shared_storage['results'].append({'result': exec_result})
                return exec_result
        
        async def run_test():
            shared_storage = {}
            node = NoFallbackAsyncNode()
            await node.run_async(shared_storage)
        
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(run_test())

    def test_async_retry_before_fallback(self):
        """Test that retries are attempted before calling async fallback"""
        async def run_test():
            shared_storage = {}
            node = AsyncFallbackNode(should_fail=True, max_retries=3)
            result = await node.run_async(shared_storage)
            return result, shared_storage
        
        result, shared_storage = self.loop.run_until_complete(run_test())
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 3)
        self.assertEqual(shared_storage['results'][0]['result'], "async_fallback")

if __name__ == '__main__':
    unittest.main()