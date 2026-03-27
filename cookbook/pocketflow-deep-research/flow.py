from pocketflow import Flow
from nodes import PlannerNode, ResearcherNode, SynthesizerNode

def create_deep_research_flow():
    """
    Create a recursive map-reduce research flow with iterative refinement.

    The flow works like this:
    1. PlannerNode generates 3 search queries for the topic
    2. ResearcherNode (BatchNode) searches the web for each query and extracts facts
    3. SynthesizerNode checks if enough info is gathered
       - If gaps remain (and under 2 loops), loops back to PlannerNode
       - Otherwise, generates the final research report

    Returns:
        Flow: A complete deep research flow
    """
    # Create node instances
    planner = PlannerNode()
    researcher = ResearcherNode()
    synthesizer = SynthesizerNode()

    # Connect the nodes: Planner -> Researcher -> Synthesizer
    planner >> researcher >> synthesizer

    # If synthesizer finds gaps, loop back to planner
    synthesizer - "research" >> planner

    return Flow(start=planner)
