import pandas as pd

from pocketflow import BatchNode


class CSVProcessor(BatchNode):
    """BatchNode that processes a large CSV file in chunks."""
    
    def __init__(self, chunk_size=1000):
        """Initialize with chunk size."""
        super().__init__()
        self.chunk_size = chunk_size
    
    def prep(self, shared):
        """Split CSV file into chunks.
        
        Returns an iterator of DataFrames, each containing chunk_size rows.
        """
        # Read CSV in chunks
        chunks = pd.read_csv(
            shared["input_file"],
            chunksize=self.chunk_size
        )
        return chunks
    
    def exec(self, prep_res):
        """Process a single chunk of the CSV.
        
        Args:
            chunk: pandas DataFrame containing chunk_size rows
            
        Returns:
            dict: Statistics for this chunk
        """
        return {
            "total_sales": prep_res["amount"].sum(),
            "num_transactions": len(prep_res),
            "total_amount": prep_res["amount"].sum()
        }
    
    def post(self, shared, prep_res, exec_res):
        """Combine results from all chunks.
        
        Args:
            prep_res: Original chunks iterator
            exec_res: List of results from each chunk
            
        Returns:
            str: Action to take next
        """
        # Combine statistics from all chunks
        total_sales = sum(res["total_sales"] for res in exec_res)
        total_transactions = sum(res["num_transactions"] for res in exec_res)
        total_amount = sum(res["total_amount"] for res in exec_res)
        
        # Calculate final statistics
        shared["statistics"] = {
            "total_sales": total_sales,
            "average_sale": total_amount / total_transactions,
            "total_transactions": total_transactions
        }
        
        return "show_stats" 