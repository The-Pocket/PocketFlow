from pocketflow import Flow
from nodes import WaitNode, CheckEmail, ProcessEmail

def create_heartbeat_flow():
    """
    Create a heartbeat monitoring flow with nested email processing.

    Outer loop: WaitNode -> EmailFlow -> WaitNode (repeats)
    Inner flow: CheckEmail -> ProcessEmail (if new emails found)

    The outer flow uses WaitNode to sleep between polling cycles. Each cycle
    runs the inner EmailFlow as a nested sub-flow. After max_cycles, WaitNode
    returns "done" to stop the loop.

    Returns:
        Flow: The heartbeat monitoring flow starting at WaitNode.
    """
    # --- Inner flow: check inbox and process any new emails ---
    check = CheckEmail()
    process = ProcessEmail()

    check - "new_email" >> process

    email_flow = Flow(start=check)

    # --- Outer flow: wait -> email_flow -> wait (loop) ---
    wait = WaitNode()

    wait >> email_flow
    email_flow >> wait

    # "done" from WaitNode has no successor, so the flow ends naturally
    return Flow(start=wait)
