import sys
from flow import create_newsletter_flow
from nodes import TOPICS

def main():
    """Run the newsletter curation pipeline."""
    # Start with default topics
    topics = list(TOPICS)

    # Add extra topics from command line if provided with --
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            topics.append(arg[2:])

    # Create and run the flow
    flow = create_newsletter_flow()

    shared = {"topics": topics}
    print(f"🤔 Curating newsletter from {len(topics)} topics...\n")
    flow.run(shared)

    print("\n📰 Newsletter:\n")
    print(shared.get("newsletter", "No newsletter generated."))

if __name__ == "__main__":
    main()
