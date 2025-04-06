import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pocketflow import Node, Flow

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

class CheckPositiveNode(Node):
   def post(self, shared_storage, prep_result, proc_result):
        if shared_storage['current'] >= 0:
            return 'positive'
        else:
            return 'negative'

class NoOpNode(Node):
    def prep(self, shared_storage):
        # Do nothing, just pass
        pass
    
class TestNode(unittest.TestCase):
    def test_single_number(self):
        shared_storage = {}
        start = NumberNode(5)
        pipeline = Flow(start=start)
        pipeline.run(shared_storage)
        self.assertEqual(shared_storage['current'], 5)

    def test_sequence(self):
        """
        Test a simple linear pipeline:
          NumberNode(5) -> AddNode(3) -> MultiplyNode(2)

        Expected result:
          (5 + 3) * 2 = 16
        """
        shared_storage = {}
        n1 = NumberNode(5)
        n2 = AddNode(3)
        n3 = MultiplyNode(2)

        # Chain them in sequence using the >> operator
        n1 >> n2 >> n3

        pipeline = Flow(start=n1)
        pipeline.run(shared_storage)

        self.assertEqual(shared_storage['current'], 16)

    def test_branching_positive(self):
        """
        Test a branching pipeline with positive route:
          start = NumberNode(5)
          check = CheckPositiveNode()
          if 'positive' -> AddNode(10)
          if 'negative' -> AddNode(-20)

        Since we start with 5, 
        check returns 'positive',
        so we add 10. Final result = 15.
        """
        shared_storage = {}
        start = NumberNode(5)
        check = CheckPositiveNode()
        add_if_positive = AddNode(10)
        add_if_negative = AddNode(-20)

        start >> check

        # Use the new dash operator for condition
        check - "positive" >> add_if_positive
        check - "negative" >> add_if_negative

        pipeline = Flow(start=start)
        pipeline.run(shared_storage)

        self.assertEqual(shared_storage['current'], 15)

    def test_negative_branch(self):
        """
        Same branching pipeline, but starting with -5.
        That should return 'negative' from CheckPositiveNode
        and proceed to add_if_negative, i.e. add -20.

        Final result: (-5) + (-20) = -25.
        """
        shared_storage = {}
        start = NumberNode(-5)
        check = CheckPositiveNode()
        add_if_positive = AddNode(10)
        add_if_negative = AddNode(-20)

        # Build the flow
        start >> check
        check - "positive" >> add_if_positive
        check - "negative" >> add_if_negative

        pipeline = Flow(start=start)
        pipeline.run(shared_storage)

        # Should have gone down the 'negative' branch
        self.assertEqual(shared_storage['current'], -25)

    def test_cycle_until_negative(self):
        """
        Demonstrate a cyclical pipeline:
        Start with 10, check if positive -> subtract 3, then go back to check.
        Repeat until the number becomes negative, at which point pipeline ends.
        """
        shared_storage = {}
        n1 = NumberNode(10)
        check = CheckPositiveNode()
        subtract3 = AddNode(-3)
        no_op = NoOpNode()  # Dummy node for the 'negative' branch

        # Build the cycle:
        #   n1 -> check -> if 'positive': subtract3 -> back to check
        n1 >> check
        check - 'positive' >> subtract3
        subtract3 >> check  
        
        # Attach a no-op node on the negative branch to avoid warning
        check - 'negative' >> no_op

        pipeline = Flow(start=n1)
        pipeline.run(shared_storage)

        # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
        self.assertEqual(shared_storage['current'], -2)


if __name__ == '__main__':
    unittest.main()
