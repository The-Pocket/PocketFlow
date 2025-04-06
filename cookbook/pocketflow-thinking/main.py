import sys
from flow import create_chain_of_thought_flow

def main():
    # Default question
    default_question = "Break a stick, then break the longer piece again. What's the probability of forming a triangle?"
    
    # Get question from command line if provided with --
    question = default_question
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            question = arg[2:]
            break
    
    print(f"🤔 Processing question: {question}")   

    # Create the flow
    cot_flow = create_chain_of_thought_flow()

    # Set up shared state
    shared = {
        "problem": question,
        "thoughts": [],
        "current_thought_number": 0,
        "total_thoughts_estimate": 10,
        "solution": None
    }
    
    # Run the flow
    cot_flow.run(shared)
    
if __name__ == "__main__":
    main()