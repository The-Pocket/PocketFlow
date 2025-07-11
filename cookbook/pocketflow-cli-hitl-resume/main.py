import json
import os
from flow import create_joke_flow

CHECKPOINT_FILE = "joke_checkpoint.json"

def main():
    """Main function to run the joke generator application."""
    joke_flow = create_joke_flow()

    if os.path.exists(CHECKPOINT_FILE):
        print("💡 Checkpoint file found. Resuming joke workflow...")
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                checkpoint_data = json.load(f)
            shared = checkpoint_data["shared"]
            resume_info = checkpoint_data["resume_info"]
            
            joke_flow.resume(shared, resume_info)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Error reading checkpoint file: {e}. Please restart.")
            os.remove(CHECKPOINT_FILE)
    else:
        print("🚀 Starting new joke workflow...")
        shared = {
            "topic": None,
            "current_joke": None,
            "disliked_jokes": [],
        }
        joke_flow.run(shared)

    print("\nThanks for using the Joke Generator!")

if __name__ == "__main__":
    main() 