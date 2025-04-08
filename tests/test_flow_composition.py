import unittest
import asyncio
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Node, Flow

# Simple example Nodes
class NumberNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def prep(self, shared_storage):
        shared_storage['current'] = self.number

class AddNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def prep(self, shared_storage):
        shared_storage['current'] += self.number

class MultiplyNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def prep(self, shared_storage):
        shared_storage['current'] *= self.number

class TestFlowComposition(unittest.TestCase):
    def test_flow_as_node(self):
        """
        1) Create a Flow (f1) starting with NumberNode(5), then AddNode(10), then MultiplyNode(2).
        2) Create a second Flow (f2) whose start is f1.
        3) Create a wrapper Flow (f3) that contains f2 to ensure proper execution.
        Expected final result in shared_storage['current']: (5 + 10) * 2 = 30.
        """
        shared_storage = {}
        
        # Inner flow f1
        f1 = Flow(start=NumberNode(5))
        f1 >> AddNode(10) >> MultiplyNode(2)
        
        # f2 starts with f1
        f2 = Flow(start=f1)
        
        # Wrapper flow f3 to ensure proper execution
        f3 = Flow(start=f2)
        f3.run(shared_storage)
        
        self.assertEqual(shared_storage['current'], 30)

    def test_nested_flow(self):
        """
        Demonstrates nested flows with proper wrapping:
        inner_flow: NumberNode(5) -> AddNode(3)
        middle_flow: starts with inner_flow -> MultiplyNode(4)
        wrapper_flow: contains middle_flow to ensure proper execution
        Expected final result: (5 + 3) * 4 = 32.
        """
        shared_storage = {}
        
        # Build the inner flow
        inner_flow = Flow(start=NumberNode(5))
        inner_flow >> AddNode(3)
        
        # Build the middle flow, whose start is the inner flow
        middle_flow = Flow(start=inner_flow)
        middle_flow >> MultiplyNode(4)
        
        # Wrapper flow to ensure proper execution
        wrapper_flow = Flow(start=middle_flow)
        wrapper_flow.run(shared_storage)
        
        self.assertEqual(shared_storage['current'], 32)

    def test_flow_chaining_flows(self):
        """
        Demonstrates chaining two flows with proper wrapping:
        flow1: NumberNode(10) -> AddNode(10) # final = 20
        flow2: MultiplyNode(2) # final = 40
        wrapper_flow: contains both flow1 and flow2 to ensure proper execution
        Expected final result: (10 + 10) * 2 = 40.
        """
        shared_storage = {}

        # flow1
        numbernode = NumberNode(10)
        numbernode >> AddNode(10)
        flow1 = Flow(start=numbernode)

        # flow2
        flow2 = Flow(start=MultiplyNode(2))

        # Chain flow1 to flow2
        flow1 >> flow2

        # Wrapper flow to ensure proper execution
        wrapper_flow = Flow(start=flow1)
        wrapper_flow.run(shared_storage)
        
        self.assertEqual(shared_storage['current'], 40)

if __name__ == '__main__':
    unittest.main()