# PocketFlow BatchNode Example

This example demonstrates the BatchNode concept in PocketFlow by implementing a CSV processor that handles large files by processing them in chunks.

## What this Example Demonstrates

- How to use BatchNode to process large inputs in chunks
- The three key methods of BatchNode:
  1. `prep`: Splits input into chunks
  2. `exec`: Processes each chunk independently
  3. `post`: Combines results from all chunks

## Project Structure
```
pocketflow-batch-node/
├── README.md
├── requirements.txt
├── data/
│   └── sales.csv      # Sample large CSV file
├── main.py            # Entry point
├── flow.py            # Flow definition
└── nodes.py           # BatchNode implementation
```

## How it Works

The example processes a large CSV file containing sales data:

1. **Chunking (prep)**: The CSV file is read and split into chunks of N rows
2. **Processing (exec)**: Each chunk is processed to calculate:
   - Total sales
   - Average sale value
   - Number of transactions
3. **Combining (post)**: Results from all chunks are aggregated into final statistics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Sample Output

```
Processing sales.csv in chunks...

Final Statistics:
- Total Sales: $1,234,567.89
- Average Sale: $123.45
- Total Transactions: 10,000
```

## Key Concepts Illustrated

1. **Chunk-based Processing**: Shows how BatchNode handles large inputs by breaking them into manageable pieces
2. **Independent Processing**: Demonstrates how each chunk is processed separately
3. **Result Aggregation**: Shows how individual results are combined into a final output 