import time
from pocketflow import Node
from utils import call_llm, check_email


class WaitNode(Node):
    def prep(self, shared):
        """Increment the heartbeat cycle counter."""
        shared["cycle"] = shared.get("cycle", 0) + 1
        print(f"\n--- 💓 Heartbeat {shared['cycle']} ---")

    def exec(self, _):
        """Sleep for the polling interval."""
        time.sleep(2)

    def post(self, shared, prep_res, exec_res):
        """Stop after max_cycles, otherwise continue the loop."""
        max_cycles = shared.get("max_cycles", 4)
        if shared["cycle"] >= max_cycles:
            print("🛑 Max cycles reached. Stopping.")
            return "done"
        # default action continues to the next node (email flow)


class CheckEmail(Node):
    def exec(self, _):
        """Check the inbox for new emails."""
        return check_email()

    def post(self, shared, prep_res, exec_res):
        """Route based on whether there are new emails."""
        if not exec_res:
            print("  📭 No new emails.")
            return None  # end inner flow — no successor needed
        shared["emails"] = exec_res
        print(f"  📬 {len(exec_res)} new email(s)!")
        return "new_email"


class ProcessEmail(Node):
    def prep(self, shared):
        """Get the emails to process."""
        return shared["emails"]

    def exec(self, emails):
        """Use the LLM to summarize each email and suggest a reply action."""
        summaries = []
        for e in emails:
            summary = call_llm(
                f"Summarize this email in one sentence and suggest a reply action.\n"
                f"From: {e['from']}\nSubject: {e['subject']}\nBody: {e['body']}"
            )
            summaries.append(summary)
        return summaries

    def post(self, shared, prep_res, exec_res):
        """Print summaries and accumulate processed results."""
        for s in exec_res:
            print(f"  💡 {s}")
        shared.setdefault("processed", []).extend(exec_res)
