import os
from flow import create_flow

def main():
    """Run the batch processing example."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create sample CSV if it doesn't exist
    if not os.path.exists("data/sales.csv"):
        print("Creating sample sales.csv...")
        import pandas as pd
        import numpy as np
        
        # Generate sample data
        np.random.seed(42)
        n_rows = 10000
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=n_rows),
            "amount": np.random.normal(100, 30, n_rows).round(2),
            "product": np.random.choice(["A", "B", "C"], n_rows)
        })
        df.to_csv("data/sales.csv", index=False)
    
    # Initialize shared store
    shared = {
        "input_file": "data/sales.csv"
    }
    
    # Create and run flow
    print(f"Processing sales.csv in chunks...")
    flow = create_flow()
    flow.run(shared)

if __name__ == "__main__":
    main() 