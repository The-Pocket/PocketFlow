import sys
from flow import create_flow


def parse_task(default_task: str) -> str:
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            return arg[2:]
    return default_task


def main():
    task = parse_task("Summarize this launch plan for a VP audience")

    shared = {
        "task": task,
        "skills_dir": "skills",
    }

    flow = create_flow()

    print(f"🧩 Task: {task}")
    flow.run(shared)

    print("\n=== Skill Used ===")
    print(shared.get("selected_skill", "(none)"))

    print("\n=== Output ===")
    print(shared.get("result", "(no result)"))


if __name__ == "__main__":
    main()
