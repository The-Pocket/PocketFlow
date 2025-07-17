import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import BatchFlow, Node


class DataProcessNode(Node):
    def prep(self, shared):
        key = self.params.get('key')
        data = shared['input_data'][key]
        if 'results' not in shared:
            shared['results'] = {}
        shared['results'][key] = data * 2

class ErrorProcessNode(Node):
    def prep(self, shared):
        key = self.params.get('key')
        if key == 'error_key':
            raise ValueError(f"Error processing key: {key}")
        if 'results' not in shared:
            shared['results'] = {}
        shared['results'][key] = True

class TestBatchFlow(unittest.TestCase):
    def setUp(self):
        self.process_node = DataProcessNode()
        
    def test_basic_batch_processing(self):
        """Test basic batch processing with multiple keys"""
        class SimpleTestBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{'key': k} for k in shared['input_data'].keys()]

        shared = {
            'input_data': {
                'a': 1,
                'b': 2,
                'c': 3
            }
        }

        flow = SimpleTestBatchFlow(start=self.process_node)
        flow.run(shared)

        expected_results = {
            'a': 2,
            'b': 4,
            'c': 6
        }
        self.assertEqual(shared['results'], expected_results)

    def test_empty_input(self):
        """Test batch processing with empty input dictionary"""
        class EmptyTestBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{'key': k} for k in shared['input_data'].keys()]

        shared = {
            'input_data': {}
        }

        flow = EmptyTestBatchFlow(start=self.process_node)
        flow.run(shared)

        self.assertEqual(shared.get('results', {}), {})

    def test_single_item(self):
        """Test batch processing with single item"""
        class SingleItemBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{'key': k} for k in shared['input_data'].keys()]

        shared = {
            'input_data': {
                'single': 5
            }
        }

        flow = SingleItemBatchFlow(start=self.process_node)
        flow.run(shared)

        expected_results = {
            'single': 10
        }
        self.assertEqual(shared['results'], expected_results)

    def test_error_handling(self):
        """Test error handling during batch processing"""
        class ErrorTestBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{'key': k} for k in shared['input_data'].keys()]

        shared = {
            'input_data': {
                'normal_key': 1,
                'error_key': 2,
                'another_key': 3
            }
        }

        flow = ErrorTestBatchFlow(start=ErrorProcessNode())
        
        with self.assertRaises(ValueError):
            flow.run(shared)

    def test_nested_flow(self):
        """Test batch processing with nested flows"""
        class InnerNode(Node):
            def exec(self, prep_res):
                key = self.params.get('key')
                if 'intermediate_results' not in shared:
                    shared['intermediate_results'] = {}
                shared['intermediate_results'][key] = shared['input_data'][key] + 1

        class OuterNode(Node):
            def exec(self, prep_res):
                key = self.params.get('key')
                if 'results' not in shared:
                    shared['results'] = {}
                shared['results'][key] = shared['intermediate_results'][key] * 2

        class NestedBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{'key': k} for k in shared['input_data'].keys()]

        # Create inner flow
        inner_node = InnerNode()
        outer_node = OuterNode()
        inner_node >> outer_node

        shared = {
            'input_data': {
                'x': 1,
                'y': 2
            }
        }

        flow = NestedBatchFlow(start=inner_node)
        flow.run(shared)

        expected_results = {
            'x': 4,  # (1 + 1) * 2
            'y': 6   # (2 + 1) * 2
        }
        self.assertEqual(shared['results'], expected_results)

    def test_custom_parameters(self):
        """Test batch processing with additional custom parameters"""
        class CustomParamNode(Node):
            def exec(self, prep_res):
                key = self.params.get('key')
                multiplier = self.params.get('multiplier', 1)
                if 'results' not in shared:
                    shared['results'] = {}
                shared['results'][key] = shared['input_data'][key] * multiplier

        class CustomParamBatchFlow(BatchFlow):
            def prep(self, shared):
                return [{
                    'key': k,
                    'multiplier': i + 1
                } for i, k in enumerate(shared['input_data'].keys())]

        shared = {
            'input_data': {
                'a': 1,
                'b': 2,
                'c': 3
            }
        }

        flow = CustomParamBatchFlow(start=CustomParamNode())
        flow.run(shared)

        expected_results = {
            'a': 1 * 1,  # first item, multiplier = 1
            'b': 2 * 2,  # second item, multiplier = 2
            'c': 3 * 3   # third item, multiplier = 3
        }
        self.assertEqual(shared['results'], expected_results)

if __name__ == '__main__':
    unittest.main()