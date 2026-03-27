import sys
from flow import create_mermaid_flow

def main():
    """Runs the PocketFlow Self-Healing Mermaid Diagram Generator."""
    print("🎨 PocketFlow Self-Healing Mermaid Generator\n")

    # Default task
    default_task = "A flowchart showing a CI/CD pipeline: code push triggers build, then parallel test and lint, then deploy to staging, manual approval, deploy to production"

    # Get task from command line if provided with --
    task = default_task
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            task = arg[2:]
            break

    print(f"🤔 Task: {task}\n")

    # Set up shared state
    shared = {
        "task": task,
    }

    # Create and run the flow
    flow = create_mermaid_flow()
    flow.run(shared)

    # Print final result
    print("\n=== Result ===")
    if "chart" in shared:
        attempts = shared.get("attempts", [])
        if attempts and len(attempts) >= 3:
            print(f"  Status: FAILED after {len(attempts)} attempts")
            print(f"  Last error: {attempts[-1]['error'][:200]}")
        else:
            retries = len(attempts)
            if retries > 0:
                print(f"  Status: SUCCESS (after {retries} retry/retries)")
            else:
                print("  Status: SUCCESS (first attempt)")
        print(f"\n  Mermaid code:\n")
        for line in shared["chart"].split("\n"):
            print(f"    {line}")
        print()

if __name__ == "__main__":
    main()
