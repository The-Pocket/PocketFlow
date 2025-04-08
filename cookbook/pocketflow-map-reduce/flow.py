from pocketflow import Flow
from nodes import ReadResumesNode, EvaluateResumesNode, ReduceResultsNode

def create_resume_processing_flow():
    """Create a map-reduce flow for processing resumes."""
    # Create nodes
    read_resumes_node = ReadResumesNode()
    evaluate_resumes_node = EvaluateResumesNode()
    reduce_results_node = ReduceResultsNode()
    
    # Connect nodes
    read_resumes_node >> evaluate_resumes_node >> reduce_results_node
    
    # Create flow
    return Flow(start=read_resumes_node)