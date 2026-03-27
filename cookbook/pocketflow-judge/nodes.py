from pocketflow import Node
import yaml
from utils import call_llm

class Generator(Node):
    def prep(self, shared):
        return {"task": shared["task"], "feedback": shared.get("feedback", "")}

    def exec(self, inputs):
        prompt = f"""Write a product description for: {inputs['task']}

The description should be clear, persuasive, and compelling. Keep it to 2-3 sentences."""
        if inputs["feedback"]:
            prompt += f"\n\nPrevious attempt was rejected. Here is the feedback:\n{inputs['feedback']}\n\nPlease improve based on this feedback."

        prompt += """

Return your response in YAML format:
```yaml
description: |
    Your product description here
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_str)
        return parsed["description"].strip()

    def post(self, shared, prep_res, exec_res):
        shared["draft"] = exec_res
        print(f"\n✍️  --- Draft (Attempt {shared.get('attempts', 0) + 1}) ---")
        print(exec_res)
        print()


class Judge(Node):
    def prep(self, shared):
        return shared["draft"]

    def exec(self, draft):
        prompt = f"""Rate this product description on a scale of 1-10 for clarity and persuasiveness.

Description:
{draft}

Return your evaluation in YAML format:
```yaml
score: 7
reasoning: |
    Brief explanation of the score
verdict: "PASS"  # Use "PASS" if score >= 7, otherwise "FAIL"
feedback: |
    Specific suggestions for improvement (only if FAIL)
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_str)
        return parsed

    def post(self, shared, prep_res, exec_res):
        score = exec_res.get("score", 0)
        verdict = exec_res.get("verdict", "FAIL")
        reasoning = exec_res.get("reasoning", "").strip()
        feedback = exec_res.get("feedback", "").strip()

        print(f"🔍 Judge Score: {score}/10")
        print(f"💡 Reasoning: {reasoning}")

        if verdict.upper() == "PASS" or score >= 7:
            print("✅ PASS - Description accepted!")
            shared["final_description"] = shared["draft"]
            shared["final_score"] = score
            return "pass"

        # Track attempts
        shared["attempts"] = shared.get("attempts", 0) + 1
        shared["feedback"] = feedback if feedback else reasoning

        if shared["attempts"] >= 3:
            print("🤔 Max attempts reached. Accepting current draft.")
            shared["final_description"] = shared["draft"]
            shared["final_score"] = score
            return "pass"

        print(f"❌ FAIL - Sending back for revision (attempt {shared['attempts']}/3)")
        print(f"📝 Feedback: {feedback}")
        return "fail"
