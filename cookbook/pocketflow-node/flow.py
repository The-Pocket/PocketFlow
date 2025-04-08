from pocketflow import Node, Flow
from utils.call_llm import call_llm

class Summarize(Node):
    def prep(self, shared):
        """Read and preprocess data from shared store."""
        return shared["data"]

    def exec(self, prep_res):
        """Execute the summarization using LLM."""
        if not prep_res:
            return "Empty text"
        prompt = f"Summarize this text in 10 words: {prep_res}"
        summary = call_llm(prompt)  # might fail
        return summary

    def exec_fallback(self, shared, prep_res, exc):
        """Provide a simple fallback instead of crashing."""
        return "There was an error processing your request."

    def post(self, shared, prep_res, exec_res):
        """Store the summary in shared store."""
        shared["summary"] = exec_res
        # Return "default" by not returning

# Create the flow
summarize_node = Summarize(max_retries=3)
flow = Flow(start=summarize_node) 