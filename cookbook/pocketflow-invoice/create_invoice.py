"""Generate a sample invoice PDF for testing the invoice processor."""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def create_sample_invoice(output_path="invoice.pdf"):
    """Creates a realistic-looking invoice PDF with line items, tax, and total."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # --- Header ---
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 60, "INVOICE")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 85, "Acme Corp")
    c.drawString(50, height - 97, "123 Business Ave, Suite 100")
    c.drawString(50, height - 109, "San Francisco, CA 94105")

    # Invoice details (right side)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 50, height - 60, "Invoice #: INV-2024-0042")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 75, "Date: 2024-11-15")
    c.drawRightString(width - 50, height - 90, "Due Date: 2024-12-15")

    # --- Bill To ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 145, "Bill To:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 160, "Widget Industries LLC")
    c.drawString(50, height - 172, "456 Client Blvd")
    c.drawString(50, height - 184, "New York, NY 10001")

    # --- Line Items Table ---
    table_top = height - 230
    col_desc = 50
    col_qty = 340
    col_price = 410
    col_amount = 500

    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#333333"))
    c.rect(45, table_top - 5, width - 90, 20, fill=False)
    c.drawString(col_desc, table_top, "Description")
    c.drawString(col_qty, table_top, "Qty")
    c.drawString(col_price, table_top, "Unit Price")
    c.drawRightString(width - 50, table_top, "Amount")

    # Line items
    items = [
        ("Web Development Services", 40, 150.00),
        ("UI/UX Design", 20, 125.00),
        ("Project Management", 10, 100.00),
        ("Quality Assurance Testing", 15, 95.00),
    ]

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    y = table_top - 25
    subtotal = 0.0

    for desc, qty, price in items:
        amount = qty * price
        subtotal += amount
        c.drawString(col_desc, y, desc)
        c.drawString(col_qty, y, str(qty))
        c.drawString(col_price, y, f"${price:,.2f}")
        c.drawRightString(width - 50, y, f"${amount:,.2f}")
        y -= 20

    # --- Totals ---
    y -= 15
    c.line(380, y + 10, width - 50, y + 10)

    c.setFont("Helvetica", 10)
    c.drawString(400, y, "Subtotal:")
    c.drawRightString(width - 50, y, f"${subtotal:,.2f}")

    tax_rate = 8.5
    tax_amount = round(subtotal * tax_rate / 100, 2)
    y -= 18
    c.drawString(400, y, f"Tax ({tax_rate}%):")
    c.drawRightString(width - 50, y, f"${tax_amount:,.2f}")

    total = subtotal + tax_amount
    y -= 22
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y, "Total:")
    c.drawRightString(width - 50, y, f"${total:,.2f}")

    # --- Footer ---
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 50, "Payment terms: Net 30 | Thank you for your business!")

    c.save()
    print(f"✅ Invoice created: {output_path}")
    print(f"   Items: {len(items)}")
    print(f"   Subtotal: ${subtotal:,.2f}")
    print(f"   Tax ({tax_rate}%): ${tax_amount:,.2f}")
    print(f"   Total: ${total:,.2f}")

if __name__ == "__main__":
    create_sample_invoice()
