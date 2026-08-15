"""Run the RLM cookbook against a local text file."""

import argparse
from pathlib import Path

from flow import create_rlm_flow


def main():
    parser = argparse.ArgumentParser(description="Summarize long context with PocketFlow RLM")
    parser.add_argument("document", type=Path, help="UTF-8 text file to analyze")
    parser.add_argument("question", help="Question to answer from the document")
    parser.add_argument("--chunk-size", type=int, default=4000)
    parser.add_argument("--max-context-chars", type=int, default=6000)
    parser.add_argument("--max-levels", type=int, default=3)
    args = parser.parse_args()

    shared = {
        "document": args.document.read_text(encoding="utf-8"),
        "question": args.question,
        "chunk_size": args.chunk_size,
        "max_context_chars": args.max_context_chars,
        "max_levels": args.max_levels,
    }
    create_rlm_flow().run(shared)
    print(shared["answer"])


if __name__ == "__main__":
    main()
