import json
import os
from pocketflow import Node
from utils.call_llm import call_llm

CHECKPOINT_FILE = "joke_checkpoint.json"

class GetTopicNode(Node):
    """Prompts the user for a joke topic."""
    def exec(self, _):
        return input("What topic would you like a joke about? ")
    def post(self, shared, _, exec_res):
        shared["topic"] = exec_res
        shared["disliked_jokes"] = []

class GenerateJokeNode(Node):
    """Generates a joke, considering previously disliked ones."""
    def prep(self, shared):
        topic = shared.get("topic")
        disliked = shared.get("disliked_jokes", [])
        prompt = f"Tell me a one-liner joke about: {topic}."
        if disliked:
            prompt += f" But don't tell me any of these: {'; '.join(disliked)}."
        return prompt
    def exec(self, prompt):
        return call_llm(prompt)
    def post(self, shared, _, exec_res):
        shared["current_joke"] = exec_res
        print(f"\nJoke: {exec_res}")

class PauseToGetFeedbackNode(Node):
    """Pauses the workflow to wait for user feedback."""
    def post(self, shared, _, exec_res):
        resume_info = {"node_id": self.node_id, "last_action": "default"}
        checkpoint_data = {"shared": shared, "resume_info": resume_info}
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(checkpoint_data, f, indent=4)
        print("\nWorkflow paused. Run the script again to provide feedback.")
        return "PAUSE"

class ProcessFeedbackNode(Node):
    """Processes user feedback and decides the next action."""
    def exec(self, shared):
        feedback = input("Did you like this joke? (yes/no): ").lower().strip()
        return "Approve" if feedback == "yes" else "Disapprove"
    def post(self, shared, _, exec_res):
        if exec_res == "Disapprove":
            joke = shared.get("current_joke")
            if joke:
                shared["disliked_jokes"].append(joke)
            print("Okay, let me try another one.")
        return exec_res

class CleanupNode(Node):
    """Cleans up the checkpoint file upon completion."""
    def exec(self, _):
        print("Great! Glad you liked it.")
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)
            print(f"Cleaned up {CHECKPOINT_FILE}.") 