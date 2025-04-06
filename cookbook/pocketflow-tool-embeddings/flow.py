from pocketflow import Flow
from nodes import EmbeddingNode

def create_embedding_flow():
    """Create a flow for text embedding"""
    # Create embedding node
    embedding = EmbeddingNode()
    
    # Create and return flow
    return Flow(start=embedding) 