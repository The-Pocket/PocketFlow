import argparse
from pocketflow import BatchNode, Flow
import collections
from utils import call_llm
import yaml

class MajorityVoteNode(BatchNode):
    def prep(self, shared):
        question = shared.get("question", "(No question provided)")
        attempts_count = shared.get("num_tries", 3)
        return [question for _ in range(attempts_count)]

    def exec(self, single_question: str):
        prompt = f"""
You are a helpful assistant. Please answer the user's question below.
Question: {single_question}

Return strictly using the following YAML structure:
```yaml
thinking: |
    (Your thinking process here)
answer: 0.123 # Final answer as a decimal with 3 decimal places
```"""
        raw_response = call_llm(prompt)
        yaml_part = raw_response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_part)

        # Validate we have at least 'answer' field
        if not isinstance(parsed, dict) or 'answer' not in parsed:
            raise RuntimeError(f"Missing 'answer' in YAML: {parsed}")

        # Return only the 'answer' field for the majority vote.
        return str(parsed['answer'])
    
    def exec_fallback(self, prep_res, exc):
        return None

    def post(self, shared, prep_res, exec_res_list):
        # Count frequency for non-None answers
        exec_res_list = [res for res in exec_res_list if res is not None]
        counter = collections.Counter(exec_res_list)
        best_answer, freq = counter.most_common(1)[0]

        # Store final
        shared["majority_answer"] = best_answer

        print("========================")
        print("All structured answers:", exec_res_list)
        print("Majority vote =>", best_answer)
        print("Frequency =>", freq)
        print("========================")

        # End the flow
        return "end"

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run majority vote reasoning on a problem")
    parser.add_argument("--problem", type=str, help="Your reasoning problem to solve")
    parser.add_argument("--tries", type=int, default=5, help="Number of attempts to make (default: 5)")
    args = parser.parse_args()
    
    # Default problem if none provided
    default_problem = """You work at a shoe factory. In front of you, there are three pairs of shoes (six individual shoes) with the following sizes: two size 4s, two size 5s, and two size 6s. The factory defines an "acceptable pair" as two shoes that differ in size by a maximum of one size (e.g., a size 5 and a size 6 would be an acceptable pair). If you close your eyes and randomly pick three pairs of shoes without replacement, what is the probability that you end up drawing three acceptable pairs?"""
    
    shared = {
        "question": args.problem if args.problem else default_problem,
        "num_tries": args.tries
    }

    majority_node = MajorityVoteNode()
    flow = Flow(start=majority_node)
    flow.run(shared)

    print("\n=== Final Answer ===")
    print(shared["majority_answer"])
    print("====================")