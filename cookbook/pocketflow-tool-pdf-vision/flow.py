from pocketflow import Flow
from nodes import ProcessPDFBatchNode

def create_vision_flow():
    """Create a flow for batch PDF processing with Vision API"""
    return Flow(start=ProcessPDFBatchNode())
