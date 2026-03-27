import sys
from flow import create_heartbeat_flow

def main():
    """Run the heartbeat email monitor."""
    # Default number of cycles
    max_cycles = 4

    # Get max cycles from command line if provided with --
    for arg in sys.argv[1:]:
        if arg.startswith("--cycles="):
            max_cycles = int(arg.split("=")[1])
            break

    # Create the flow
    flow = create_heartbeat_flow()

    # Run with shared store
    shared = {"max_cycles": max_cycles}
    print("🚀 Starting Heartbeat Email Monitor")
    print(f"   Polling every 2 seconds for {max_cycles} cycles...\n")
    flow.run(shared)

    print("\n✅ Monitor stopped.")
    processed = shared.get("processed", [])
    print(f"📊 Total emails processed: {len(processed)}")

if __name__ == "__main__":
    main()
