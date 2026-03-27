import sys
from flow import create_deep_research_flow

def main():
    """Run the deep research flow on a given topic."""
    # Default topic
    default_topic = "The current state of quantum computing in 2025"

    # Get topic from command line if provided with --
    topic = default_topic
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            topic = arg[2:]
            break

    # Create and run the flow
    flow = create_deep_research_flow()

    shared = {"topic": topic}
    print(f"🤔 Researching: {topic}\n")
    flow.run(shared)

    print("\n📄 Final Report:\n")
    print(shared.get("report", "No report generated."))

if __name__ == "__main__":
    main()
