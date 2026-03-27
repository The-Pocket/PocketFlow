from pocketflow import Flow
from nodes import AdvocateFor, AdvocateAgainst, JudgeDebate

def create_debate_flow():
    # Create node instances
    advocate_for = AdvocateFor(max_retries=3, wait=10)
    advocate_against = AdvocateAgainst(max_retries=3, wait=10)
    judge = JudgeDebate(max_retries=3, wait=10)

    # Connect nodes in sequence: FOR -> AGAINST -> JUDGE
    advocate_for >> advocate_against >> judge

    # Create flow starting with advocate_for
    debate_flow = Flow(start=advocate_for)
    return debate_flow
