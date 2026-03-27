import sys
import os
from flow import create_invoice_flow

def main():
    """Runs the PocketFlow Invoice Processor."""
    print("🧾 PocketFlow Invoice Processor\n")

    # Get PDF path from command line args (--path=invoice.pdf)
    pdf_path = "invoice.pdf"
    for arg in sys.argv[1:]:
        if arg.startswith("--path="):
            pdf_path = arg[len("--path="):]
            break

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        print("Run 'python create_invoice.py' first to generate a sample invoice.")
        sys.exit(1)

    print(f"📄 Processing: {pdf_path}\n")

    # Set up shared state
    shared = {
        "pdf_path": pdf_path,
    }

    # Create and run the flow
    flow = create_invoice_flow()
    flow.run(shared)

    # Print summary
    print("\n=== Summary ===")
    if "extracted" in shared:
        data = shared["extracted"]
        print(f"  Invoice #: {data.get('invoice_number')}")
        print(f"  Total: ${data.get('total', 0):.2f}")

    if "validation_errors" in shared:
        errors = shared["validation_errors"]
        if errors:
            print(f"  Status: FAILED ({len(errors)} error(s))")
        else:
            print("  Status: PASSED ✅")

if __name__ == "__main__":
    main()
