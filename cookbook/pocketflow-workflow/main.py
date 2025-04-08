from flow import create_article_flow

def run_flow(topic="AI Safety"):
    """
    Run the article writing workflow with a specific topic
    
    Args:
        topic (str): The topic for the article
    """
    # Initialize shared data with the topic
    shared = {"topic": topic}
    
    # Print starting message
    print(f"\n=== Starting Article Workflow on Topic: {topic} ===\n")
    
    # Run the flow
    flow = create_article_flow()
    flow.run(shared)
    
    # Output summary
    print("\n=== Workflow Completed ===\n")
    print(f"Topic: {shared['topic']}")
    print(f"Outline Length: {len(shared['outline'])} characters")
    print(f"Draft Length: {len(shared['draft'])} characters")
    print(f"Final Article Length: {len(shared['final_article'])} characters")
    
    return shared

if __name__ == "__main__":
    import sys
    
    # Get topic from command line if provided
    topic = "AI Safety"  # Default topic
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    
    run_flow(topic)