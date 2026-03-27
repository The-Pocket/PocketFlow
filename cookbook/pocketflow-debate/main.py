import sys
from flow import create_debate_flow

def main():
    # Default claim
    default_claim = "Remote work is more productive than office work"

    # Get claim from command line if provided with --
    claim = default_claim
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            claim = arg[2:]
            break

    print(f"🤔 Debating claim: \"{claim}\"")

    # Create the flow
    debate_flow = create_debate_flow()

    # Set up shared state
    shared = {
        "claim": claim
    }

    # Run the flow
    debate_flow.run(shared)

    # Print final summary
    print(f"\n=== Debate Summary ===")
    print(f"📋 Claim: \"{shared['claim']}\"")
    print(f"🏆 Winner: {shared.get('winner', 'N/A')}")
    print(f"📊 Scores - FOR: {shared.get('score_for', 'N/A')}/10 | AGAINST: {shared.get('score_against', 'N/A')}/10")
    print(f"⚖️  Verdict: {shared.get('verdict', 'N/A')}")
    print("======================")

if __name__ == "__main__":
    main()
