from pocketflow import Flow
from nodes import DecideAction, ReadDoc, Answer

def create_agentic_rag_flow():
    """
    Create an agentic RAG flow.

    The agent reads document summaries and decides what to dive into:
      DecideAction --read--> ReadDoc --decide--> DecideAction
      DecideAction --answer--> Answer

    Returns:
        Flow: The agentic RAG flow starting at DecideAction.
    """
    decide = DecideAction()
    read = ReadDoc()
    answer = Answer()

    # If DecideAction returns "read", go to ReadDoc
    decide - "read" >> read

    # If DecideAction returns "answer", go to Answer
    decide - "answer" >> answer

    # After ReadDoc, loop back to DecideAction
    read - "decide" >> decide

    return Flow(start=decide)
