from pocketflow import Node
import yaml
from utils import call_llm

class AdvocateFor(Node):
    def prep(self, shared):
        return shared["claim"]

    def exec(self, claim):
        prompt = f"""You are an expert advocate arguing FOR this claim. Be specific, use evidence and logical reasoning.

Claim: "{claim}"

Present your strongest case in 3-4 sentences.

Return your response in YAML format:
```yaml
argument: |
    Your argument here
key_points:
    - First key point
    - Second key point
    - Third key point
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_str)
        return parsed

    def post(self, shared, prep_res, exec_res):
        argument = exec_res.get("argument", "").strip()
        key_points = exec_res.get("key_points", [])
        shared["case_for"] = argument
        shared["case_for_points"] = key_points
        print(f"\n🟢 --- Advocate FOR ---")
        print(argument)
        print(f"💡 Key points:")
        for point in key_points:
            print(f"   - {point}")
        print()


class AdvocateAgainst(Node):
    def prep(self, shared):
        return {"claim": shared["claim"], "opposing": shared["case_for"]}

    def exec(self, inputs):
        prompt = f"""You are an expert advocate arguing AGAINST this claim. Rebut the opposing argument and present strong counterarguments.

Claim: "{inputs['claim']}"

Your opponent argued:
{inputs['opposing']}

Rebut their points and present your strongest counterarguments in 3-4 sentences.

Return your response in YAML format:
```yaml
argument: |
    Your counterargument here
key_points:
    - First key rebuttal point
    - Second key rebuttal point
    - Third key rebuttal point
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_str)
        return parsed

    def post(self, shared, prep_res, exec_res):
        argument = exec_res.get("argument", "").strip()
        key_points = exec_res.get("key_points", [])
        shared["case_against"] = argument
        shared["case_against_points"] = key_points
        print(f"🔴 --- Advocate AGAINST ---")
        print(argument)
        print(f"💡 Key points:")
        for point in key_points:
            print(f"   - {point}")
        print()


class JudgeDebate(Node):
    def prep(self, shared):
        return {
            "claim": shared["claim"],
            "case_for": shared["case_for"],
            "case_against": shared["case_against"]
        }

    def exec(self, inputs):
        prompt = f"""You are an impartial judge evaluating a debate.

Claim: "{inputs['claim']}"

Argument FOR:
{inputs['case_for']}

Argument AGAINST:
{inputs['case_against']}

Which argument is stronger? Evaluate the quality of reasoning, evidence, and persuasiveness of each side.

Return your verdict in YAML format:
```yaml
winner: "FOR"  # or "AGAINST"
score_for: 7  # 1-10
score_against: 6  # 1-10
verdict: |
    Your one-sentence explanation of the decision
reasoning: |
    Brief analysis of both arguments' strengths and weaknesses
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_str)
        return parsed

    def post(self, shared, prep_res, exec_res):
        winner = exec_res.get("winner", "Unknown")
        score_for = exec_res.get("score_for", "N/A")
        score_against = exec_res.get("score_against", "N/A")
        verdict = exec_res.get("verdict", "").strip()
        reasoning = exec_res.get("reasoning", "").strip()

        shared["verdict"] = verdict
        shared["winner"] = winner
        shared["score_for"] = score_for
        shared["score_against"] = score_against
        shared["reasoning"] = reasoning

        print(f"⚖️  --- VERDICT ---")
        print(f"🏆 Winner: {winner}")
        print(f"📊 Scores - FOR: {score_for}/10 | AGAINST: {score_against}/10")
        print(f"💬 {verdict}")
        print(f"🔍 {reasoning}")
