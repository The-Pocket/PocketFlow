import sys
from flow import create_agentic_rag_flow

def main():
    """Run the agentic RAG example."""
    # Default question
    default_question = "How do nodes work in PocketFlow?"

    # Get question from command line if provided with --
    question = default_question
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            question = arg[2:]
            break

    # Create the flow
    flow = create_agentic_rag_flow()

    # Run with shared store
    shared = {"question": question}
    print(f"🤔 Question: {question}\n")
    flow.run(shared)

    print(f"\n🎯 Final Answer:")
    print(shared.get("answer", "No answer generated."))

if __name__ == "__main__":
    main()
