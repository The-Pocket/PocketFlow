import sys
from flow import create_agent_flow

def main():
    """Simple function to process a question with supervised answers."""
    # Default question
    default_question = "Who won the Nobel Prize in Physics 2024?"
    
    # Get question from command line if provided with --
    question = default_question
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            question = arg[2:]
            break
    
    # Create the agent flow with supervision
    agent_flow = create_agent_flow()
    
    # Process the question
    shared = {"question": question}
    print(f"🤔 Processing question: {question}")
    agent_flow.run(shared)
    print("\n🎯 Final Answer:")
    print(shared.get("answer", "No answer found"))

if __name__ == "__main__":
    main()