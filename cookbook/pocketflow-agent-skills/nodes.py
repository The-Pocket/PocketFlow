from pocketflow import Node
from utils import call_llm, load_skills


class SelectSkill(Node):
    def prep(self, shared):
        return {
            "task": shared["task"],
            "skills": load_skills(shared["skills_dir"]),
        }

    def exec(self, prep_res):
        task = prep_res["task"].lower()
        skills = prep_res["skills"]

        # Tiny deterministic router for demo purposes.
        if "checklist" in task or "steps" in task:
            preferred = "checklist_writer"
        else:
            preferred = "executive_brief"

        if preferred in skills:
            return preferred, skills[preferred]

        # fallback: first available skill
        name, content = next(iter(skills.items()))
        return name, content

    def post(self, shared, prep_res, exec_res):
        skill_name, skill_content = exec_res
        shared["selected_skill"] = skill_name
        shared["selected_skill_content"] = skill_content
        return "default"


class ApplySkill(Node):
    def prep(self, shared):
        return {
            "task": shared["task"],
            "skill_name": shared["selected_skill"],
            "skill_content": shared["selected_skill_content"],
        }

    def exec(self, prep_res):
        prompt = f"""
You are running an Agent Skill.

Skill name: {prep_res['skill_name']}

Skill instructions:
---
{prep_res['skill_content']}
---

User task:
{prep_res['task']}

Follow the skill instructions exactly and return the final result only.
""".strip()
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "default"
