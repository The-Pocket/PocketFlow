"""Run the minimal RLM cookbook against a local UTF-8 text file."""

import argparse
from pathlib import Path

from flow import create_rlm_flow


def main():
    parser = argparse.ArgumentParser(description="Explore long context with PocketFlow RLM")
    parser.add_argument("document", type=Path, help="UTF-8 text file to analyze")
    parser.add_argument("question", help="Question to answer from the document")
    parser.add_argument("--max-iterations", type=int, default=6)
    parser.add_argument("--max-code-chars", type=int, default=8000)
    args = parser.parse_args()

    shared = {
        "context": args.document.read_text(encoding="utf-8"),
        "question": args.question,
        "max_iterations": args.max_iterations,
        "max_code_chars": args.max_code_chars,
    }
    create_rlm_flow().run(shared)
    print(shared["answer"])


if __name__ == "__main__":
    main()
