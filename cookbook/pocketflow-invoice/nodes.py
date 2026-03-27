import yaml
import base64
import fitz  # PyMuPDF
from pocketflow import Node
from utils import call_llm_with_image

class ExtractFields(Node):
    """Extracts structured invoice data from a PDF using GPT-4o vision."""

    def prep(self, shared):
        return shared["pdf_path"]

    def exec(self, pdf_path):
        print("🔍 Converting PDF to image...")
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        image_bytes = pix.tobytes("png")
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        doc.close()

        print("🤔 Extracting invoice fields with GPT-4o vision...")
        prompt = """Extract all fields from this invoice image. Output ONLY yaml:
```yaml
invoice_number: "..."
vendor: "..."
customer: "..."
date: "..."
due_date: "..."
line_items:
  - description: "..."
    quantity: 1
    unit_price: 0.00
    amount: 0.00
subtotal: 0.00
tax_rate: 0.0
tax_amount: 0.00
total: 0.00
```"""
        resp = call_llm_with_image(prompt, image_base64)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        return yaml.safe_load(yaml_str)

    def post(self, shared, prep_res, exec_res):
        # Coerce numeric fields to float (LLM may return strings with commas)
        def to_float(v):
            if isinstance(v, (int, float)):
                return float(v)
            return float(str(v).replace(",", "").replace("$", ""))

        for key in ("subtotal", "tax_rate", "tax_amount", "total"):
            if key in exec_res:
                exec_res[key] = to_float(exec_res[key])
        for item in exec_res.get("line_items", []):
            for key in ("quantity", "unit_price", "amount"):
                if key in item:
                    item[key] = to_float(item[key])

        shared["extracted"] = exec_res
        print("  Extracted fields:")
        print(f"    Invoice #: {exec_res.get('invoice_number')}")
        print(f"    Vendor: {exec_res.get('vendor')}")
        print(f"    Customer: {exec_res.get('customer')}")
        items = exec_res.get("line_items", [])
        print(f"    Line items: {len(items)}")
        for item in items:
            print(f"      - {item['description']}: {item['quantity']:.0f} x ${item['unit_price']:.2f} = ${item['amount']:.2f}")
        print(f"    Subtotal: ${exec_res.get('subtotal', 0):.2f}")
        print(f"    Tax: ${exec_res.get('tax_amount', 0):.2f}")
        print(f"    Total: ${exec_res.get('total', 0):.2f}")


class Validate(Node):
    """Validates invoice math: line item amounts, subtotal, tax, and total."""

    def prep(self, shared):
        return shared["extracted"]

    def exec(self, data):
        print("🔍 Validating invoice math...")
        errors = []

        # Validate each line item: quantity * unit_price == amount
        items = data.get("line_items", [])
        for item in items:
            expected = round(item["quantity"] * item["unit_price"], 2)
            if abs(expected - item["amount"]) > 0.01:
                errors.append(
                    f"Line item '{item['description']}' math error: "
                    f"{item['quantity']} x ${item['unit_price']:.2f} = ${expected:.2f}, "
                    f"but invoice says ${item['amount']:.2f}"
                )

        # Validate subtotal: sum of line item amounts
        computed_subtotal = sum(item["amount"] for item in items)
        if abs(computed_subtotal - data["subtotal"]) > 0.01:
            errors.append(
                f"Subtotal mismatch: items sum to ${computed_subtotal:.2f}, "
                f"invoice says ${data['subtotal']:.2f}"
            )

        # Validate tax: subtotal * tax_rate
        tax_pct = data["tax_rate"] if data["tax_rate"] > 1 else data["tax_rate"] * 100
        computed_tax = round(data["subtotal"] * tax_pct / 100, 2)
        if abs(computed_tax - data["tax_amount"]) > 0.01:
            errors.append(
                f"Tax mismatch: ${data['subtotal']:.2f} x {tax_pct}% = ${computed_tax:.2f}, "
                f"invoice says ${data['tax_amount']:.2f}"
            )

        # Validate total: subtotal + tax_amount
        computed_total = data["subtotal"] + data["tax_amount"]
        if abs(computed_total - data["total"]) > 0.01:
            errors.append(
                f"Total mismatch: ${data['subtotal']:.2f} + ${data['tax_amount']:.2f} = ${computed_total:.2f}, "
                f"invoice says ${data['total']:.2f}"
            )

        return errors

    def post(self, shared, prep_res, exec_res):
        shared["validation_errors"] = exec_res
        if exec_res:
            print("  Validation FAILED:")
            for err in exec_res:
                print(f"    - {err}")
        else:
            print("  Validation passed ✅")
