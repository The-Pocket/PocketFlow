from pocketflow import Flow, Node
from nodes import CSVProcessor

class ShowStats(Node):
    """Node to display the final statistics."""
    
    def prep(self, shared):
        """Get statistics from shared store."""
        return shared["statistics"]
    
    def post(self, shared, prep_res, exec_res):
        """Display the statistics."""
        stats = prep_res
        print("\nFinal Statistics:")
        print(f"- Total Sales: ${stats['total_sales']:,.2f}")
        print(f"- Average Sale: ${stats['average_sale']:,.2f}")
        print(f"- Total Transactions: {stats['total_transactions']:,}\n")
        return "end"

def create_flow():
    """Create and return the processing flow."""
    # Create nodes
    processor = CSVProcessor(chunk_size=1000)
    show_stats = ShowStats()
    
    # Connect nodes
    processor - "show_stats" >> show_stats
    
    # Create and return flow
    return Flow(start=processor) 