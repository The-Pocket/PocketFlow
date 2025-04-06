from flow import flow

def main():
    # Example text to summarize
    text = """
    PocketFlow is a minimalist LLM framework that models workflows as a Nested Directed Graph.
    Nodes handle simple LLM tasks, connecting through Actions for Agents.
    Flows orchestrate these nodes for Task Decomposition, and can be nested.
    It also supports Batch processing and Async execution.
    """

    # Initialize shared store
    shared = {"data": text}
    
    # Run the flow
    flow.run(shared)
    
    # Print result
    print("\nInput text:", text)
    print("\nSummary:", shared["summary"])

if __name__ == "__main__":
    main() 