import sys
from flow import create_lead_generation_flow


def main():
    """Run the lead-generation pipeline."""
    # Default product is defined in utils.py; users can override leads via shared store
    # Accept an optional --product flag for display purposes
    product_override = None
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            product_override = arg[2:]
            break

    flow = create_lead_generation_flow()
    shared = {}

    print("🚀 Starting Lead-Generation Pipeline")
    print("=" * 50)

    print("\n📋 Step 1 — Scraping leads")
    print("🔍 Step 2 — Enriching leads")
    print("🤔 Step 3 — Scoring leads with LLM")
    print("✍️  Step 4 — Personalizing emails\n")

    flow.run(shared)

    # Print results
    print("\n" + "=" * 50)
    print("📧 Generated Emails")
    print("=" * 50)
    for item in shared.get("emails", []):
        lead = item["lead"]
        print(f"\n--- {lead['name']} ({lead['title']} @ {lead['company']}) | Score: {lead['score']}/10 ---")
        print(item["email"])
        print()


if __name__ == "__main__":
    main()
