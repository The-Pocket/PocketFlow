"""Flow configuration for the communication example."""

from pocketflow import Flow
from nodes import TextInput, WordCounter, ShowStats, EndNode

def create_flow():
    """Create and configure the flow with all nodes."""
    # Create nodes
    text_input = TextInput()
    word_counter = WordCounter()
    show_stats = ShowStats()
    end_node = EndNode()
    
    # Configure transitions
    text_input - "count" >> word_counter
    word_counter - "show" >> show_stats
    show_stats - "continue" >> text_input
    text_input - "exit" >> end_node
    
    # Create and return flow
    return Flow(start=text_input) 