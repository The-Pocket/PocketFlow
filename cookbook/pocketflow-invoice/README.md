# Invoice Processor

A PocketFlow cookbook example that extracts structured data from PDF invoices using GPT-4o vision, then validates the math (line items, tax, and totals).

## Features

- **PDF Vision Extraction**: Converts invoice PDFs to images and uses GPT-4o vision to extract structured fields
- **Math Validation**: Verifies line item amounts, subtotal, tax calculations, and grand total
- **Sample Invoice Generator**: Includes a helper script to create a realistic test invoice PDF

## Getting Started

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set your OpenAI API key:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```

    Quick check to make sure your API key works:
    ```bash
    python utils.py
    ```

3. Generate a sample invoice PDF:
    ```bash
    python create_invoice.py
    ```

4. Run the invoice processor:
    ```bash
    python main.py
    ```

    Or specify a custom PDF path:
    ```bash
    python main.py --path=my_invoice.pdf
    ```

## How It Works

```mermaid
flowchart LR
    extract[ExtractFields] --> validate[Validate]
```

1. **ExtractFields**: Converts the PDF to an image using PyMuPDF, sends it to GPT-4o vision, and extracts structured invoice data (vendor, customer, line items, tax, total) as YAML
2. **Validate**: Checks the math -- verifies each line item (qty x unit_price = amount), subtotal (sum of amounts), tax (subtotal x rate), and grand total (subtotal + tax)

## Files

- [`main.py`](./main.py): Entry point with CLI argument parsing
- [`flow.py`](./flow.py): Defines the invoice processing flow
- [`nodes.py`](./nodes.py): ExtractFields and Validate node implementations
- [`utils.py`](./utils.py): OpenAI GPT-4o and vision API wrappers
- [`create_invoice.py`](./create_invoice.py): Generates a sample invoice PDF for testing
- [`requirements.txt`](./requirements.txt): Python dependencies

## Example Output

```
🧾 PocketFlow Invoice Processor

📄 Processing: invoice.pdf

🔍 Converting PDF to image...
🤔 Extracting invoice fields with GPT-4o vision...
  Extracted fields:
    Invoice #: INV-2024-0042
    Vendor: Acme Corp
    Customer: Widget Industries LLC
    Line items: 4
      - Web Development Services: 40 x $150.00 = $6000.00
      - UI/UX Design: 20 x $125.00 = $2500.00
      - Project Management: 10 x $100.00 = $1000.00
      - Quality Assurance Testing: 15 x $95.00 = $1425.00
    Subtotal: $10925.00
    Tax: $928.62
    Total: $11853.62
🔍 Validating invoice math...
  Validation passed ✅

=== Summary ===
  Invoice #: INV-2024-0042
  Total: $11853.62
  Status: PASSED ✅
```
