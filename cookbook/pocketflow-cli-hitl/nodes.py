from pocketflow import Node
from utils.call_llm import call_llm


class GetTopicNode(Node):
    """Prompts the user to enter the topic for the joke."""
    def exec(self, prep_res):
        return input("What topic would you like a joke about? ")

    def post(self, shared, prep_res, exec_res):
        shared["topic"] = exec_res

class GenerateJokeNode(Node):
    """Generates a joke based on the topic and any previous feedback."""
    def prep(self, shared):
        topic = shared.get("topic", "anything")
        disliked_jokes = shared.get("disliked_jokes", [])
        
        prompt = f"Please generate an one-liner joke about: {topic}. Make it short and funny."
        if disliked_jokes:
            disliked_str = "; ".join(disliked_jokes)
            prompt = f"The user did not like the following jokes: [{disliked_str}]. Please generate a new, different joke about {topic}."
        return prompt

    def exec(self, prep_res):
        return call_llm(prep_res)

    def post(self, shared, prep_res, exec_res):
        shared["current_joke"] = exec_res
        print(f"\nJoke: {exec_res}")

class GetFeedbackNode(Node):
    """Presents the joke to the user and asks for approval."""
    def exec(self, prep_res):
        while True:
            feedback = input("Did you like this joke? (yes/no): ").strip().lower()
            if feedback in ["yes", "y", "no", "n"]:
                return feedback
            print("Invalid input. Please type 'yes' or 'no'.")

    def post(self, shared, prep_res, exec_res):
        if exec_res in ["yes", "y"]:
            shared["user_feedback"] = "approve"
            print("Great! Glad you liked it.")
            return "Approve"
        else:
            shared["user_feedback"] = "disapprove"
            current_joke = shared.get("current_joke")
            if current_joke:
                if "disliked_jokes" not in shared:
                    shared["disliked_jokes"] = []
                shared["disliked_jokes"].append(current_joke)
            print("Okay, let me try another one.")
            return "Disapprove" 