from pocketflow import Flow
from nodes import ChainOfThoughtNode

def create_chain_of_thought_flow():
    # Create a ChainOfThoughtNode
    cot_node = ChainOfThoughtNode()
    
    # Connect the node to itself for the "continue" action
    cot_node - "continue" >> cot_node
    
    # Create the flow
    cot_flow = Flow(start=cot_node)
    return cot_flow