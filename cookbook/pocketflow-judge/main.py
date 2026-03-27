import sys
from flow import create_judge_flow

def main():
    # Default product
    default_task = "A noise-cancelling wireless headphone with 30-hour battery life"

    # Get task from command line if provided with --
    task = default_task
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            task = arg[2:]
            break

    print(f"🤔 Generating product description for: {task}")

    # Create the flow
    judge_flow = create_judge_flow()

    # Set up shared state
    shared = {
        "task": task,
        "attempts": 0
    }

    # Run the flow
    judge_flow.run(shared)

    # Print final result
    print("\n=== Final Result ===")
    print(f"📝 Description: {shared.get('final_description', 'N/A')}")
    print(f"⭐ Score: {shared.get('final_score', 'N/A')}/10")
    print("====================")

if __name__ == "__main__":
    main()
