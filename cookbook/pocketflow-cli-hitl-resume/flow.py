from pocketflow import Flow
from nodes import (
    GetTopicNode,
    GenerateJokeNode,
    PauseToGetFeedbackNode,
    ProcessFeedbackNode,
    CleanupNode,
)

def create_joke_flow():
    """Creates the joke generation flow with a pause/resume loop."""
    get_topic = GetTopicNode(node_id="get_topic")
    generate_joke = GenerateJokeNode(node_id="generate_joke")
    pause = PauseToGetFeedbackNode(node_id="pause")
    process_feedback = ProcessFeedbackNode(node_id="process_feedback")
    cleanup = CleanupNode(node_id="cleanup")

    # Initial run path: Get topic -> Generate joke -> Pause
    get_topic >> generate_joke >> pause

    # Resume path: After pausing, the next step is to process feedback.
    pause >> process_feedback

    # Feedback loop: If disapproved, generate a new joke and pause again.
    process_feedback - "Disapprove" >> generate_joke
    # If approved, clean up and end the flow.
    process_feedback - "Approve" >> cleanup

    return Flow(start=get_topic) 