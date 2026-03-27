from pocketflow import Flow
from nodes import Generator, Judge

def create_judge_flow():
    # Create node instances
    generator = Generator(max_retries=3, wait=10)
    judge = Judge(max_retries=3, wait=10)

    # Connect nodes: Generator -> Judge, Judge --fail--> Generator (loop)
    generator >> judge
    judge - "fail" >> generator

    # Create flow starting with generator
    judge_flow = Flow(start=generator)
    return judge_flow
