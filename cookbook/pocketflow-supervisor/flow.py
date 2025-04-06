from pocketflow import Flow
from nodes import DecideAction, SearchWeb, UnreliableAnswerNode, SupervisorNode

def create_agent_inner_flow():
    """
    Create the inner research agent flow without supervision.
    
    This flow handles the research cycle:
    1. DecideAction node decides whether to search or answer
    2. If search, go to SearchWeb node and return to decide
    3. If answer, go to UnreliableAnswerNode
    
    Returns:
        Flow: A research agent flow
    """
    # Create instances of each node
    decide = DecideAction()
    search = SearchWeb()
    answer = UnreliableAnswerNode()
    
    # Connect the nodes
    # If DecideAction returns "search", go to SearchWeb
    decide - "search" >> search
    
    # If DecideAction returns "answer", go to UnreliableAnswerNode
    decide - "answer" >> answer
    
    # After SearchWeb completes and returns "decide", go back to DecideAction
    search - "decide" >> decide
    
    # Create and return the inner flow, starting with the DecideAction node
    return Flow(start=decide)

def create_agent_flow():
    """
    Create a supervised agent flow by treating the entire agent flow as a node
    and placing the supervisor outside of it.
    
    The flow works like this:
    1. Inner agent flow does research and generates an answer
    2. SupervisorNode checks if the answer is valid
    3. If answer is valid, flow completes
    4. If answer is invalid, restart the inner agent flow
    
    Returns:
        Flow: A complete research agent flow with supervision
    """
    # Create the inner flow
    agent_flow = create_agent_inner_flow()
    
    # Create the supervisor node
    supervisor = SupervisorNode()
    
    # Connect the components
    # After agent_flow completes, go to supervisor
    agent_flow >> supervisor
    
    # If supervisor rejects the answer, go back to agent_flow
    supervisor - "retry" >> agent_flow
    
    # Create and return the outer flow, starting with the agent_flow
    return Flow(start=agent_flow) 