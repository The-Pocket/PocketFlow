from pocketflow import Flow
from nodes import ExtractFields, Validate

def create_invoice_flow():
    """Creates and returns the invoice processing flow."""
    # Create nodes
    extract = ExtractFields(max_retries=3, wait=5)
    validate = Validate()

    # Define transitions: extract -> validate
    extract >> validate

    # Create flow starting with extraction
    return Flow(start=extract)
