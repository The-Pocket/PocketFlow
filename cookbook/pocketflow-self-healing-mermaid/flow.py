from pocketflow import Flow
from nodes import WriteChart, CompileChart

def create_mermaid_flow():
    """Creates and returns the self-healing Mermaid diagram flow."""
    # Create nodes
    write_chart = WriteChart(max_retries=3, wait=5)
    compile_chart = CompileChart()

    # Define transitions
    write_chart >> compile_chart
    compile_chart - "fix" >> write_chart

    # Create flow starting with chart generation
    return Flow(start=write_chart)
