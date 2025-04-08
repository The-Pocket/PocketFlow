from flow import create_vision_flow

def main():
    # Create and run flow
    flow = create_vision_flow()
    shared = {}
    flow.run(shared)
    
    # Print results
    if "results" in shared:
        for result in shared["results"]:
            print(f"\nFile: {result['filename']}")
            print("-" * 50)
            print(result["text"])

if __name__ == "__main__":
    main()
