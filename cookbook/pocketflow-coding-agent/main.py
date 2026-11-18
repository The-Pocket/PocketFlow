import sys
from flow import create_coding_agent_flow
from setup_test_project import setup_test_project, WORKDIR

def main():
    default_task = (
        "Implement the skeleton functions to make all tests pass. "
        "Run: python -m pytest test_tokenizer.py test_parser.py test_executor.py -v"
    )
    task = default_task
    grf_acceptance = "--grf-acceptance" in sys.argv[1:]
    for arg in sys.argv[1:]:
        if arg.startswith("--") and arg != "--grf-acceptance":
            task = arg[2:]
            break

    setup_test_project()
    flow = create_coding_agent_flow()
    shared = {"task": task, "workdir": WORKDIR, "grf_acceptance": grf_acceptance}
    print(f"🤖 Coding Agent starting...")
    print(f"📋 Task: {task}")
    print(f"📁 Working in: {WORKDIR}\n")
    flow.run(shared)
    print(f"\n🎯 Result: {shared.get('result', '')}")

if __name__ == "__main__":
    main()
