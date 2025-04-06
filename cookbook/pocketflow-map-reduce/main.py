from flow import create_resume_processing_flow

def main():
    # Initialize shared store
    shared = {}
    
    # Create the resume processing flow
    resume_flow = create_resume_processing_flow()
    
    # Run the flow
    print("Starting resume qualification processing...")
    resume_flow.run(shared)
    
    # Display final summary information (additional to what's already printed in ReduceResultsNode)
    if "summary" in shared:
        print("\nDetailed evaluation results:")
        for filename, evaluation in shared.get("evaluations", {}).items():
            qualified = "✓" if evaluation.get("qualifies", False) else "✗"
            name = evaluation.get("candidate_name", "Unknown")
            print(f"{qualified} {name} ({filename})")
    
    print("\nResume processing complete!")

if __name__ == "__main__":
    main()