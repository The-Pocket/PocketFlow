import os
from flow import create_flow

def main():
    """Run the web crawler flow"""
    
    # Get website URL from user
    url = input("Enter website URL to crawl (e.g., https://example.com): ")
    if not url:
        print("Error: URL is required")
        return
        
    # Initialize shared data
    shared = {
        "base_url": url,
        "max_pages": 1
    }
    
    # Create and run flow
    flow = create_flow()
    flow.run(shared)
    
    # Results are in shared["report"]
    
if __name__ == "__main__":
    main()
