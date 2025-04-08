from flow import create_flow

def main():
    """Run the communication example."""
    flow = create_flow()
    shared = {}
    flow.run(shared)

if __name__ == "__main__":
    main() 