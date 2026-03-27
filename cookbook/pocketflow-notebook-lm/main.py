import sys
from flow import create_podcast_flow
from utils import DOCS


def main():
    """Generate a podcast from documents."""
    # Accept an optional --output flag for the output filename
    output_file = "podcast.mp3"
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            output_file = arg[2:]
            break

    flow = create_podcast_flow()
    shared = {
        "docs": DOCS,
        "output_file": output_file,
    }

    print("🎧 Starting Podcast Generation Pipeline")
    print("=" * 50)
    print(f"  📄 {len(DOCS)} source documents")
    print(f"  💾 Output: {output_file}")
    print()

    print("🔍 Step 1 — Analyzing documents for interesting nuggets")
    print("✍️  Step 2 — Writing conversational podcast script")
    print("🎙️  Step 3 — Converting script to audio with TTS")
    print()

    flow.run(shared)

    print("\n" + "=" * 50)
    print(f"🎧 Podcast saved to: {shared.get('audio_file', output_file)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
