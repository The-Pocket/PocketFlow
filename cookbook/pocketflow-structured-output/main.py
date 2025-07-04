import yaml
import os  # Needed for the utils import below
from pocketflow import Node, Flow
from utils import call_llm # Assumes utils.py with call_llm exists

class ResumeParserNode(Node):
    def prep(self, shared):
        """Return resume text and target skills from shared state."""
        return {
            "resume_text": shared["resume_text"],
            "target_skills": shared.get("target_skills", [])
        }

    def exec(self, prep_res):
        """Extract structured data from resume using prompt engineering.
        Requests YAML output with comments and skill indexes as a list.
        """
        resume_text = prep_res["resume_text"]
        target_skills = prep_res["target_skills"]

        # Format skills with indexes for the prompt
        skill_list_for_prompt = "\n".join([f"{i}: {skill}" for i, skill in enumerate(target_skills)])

        # Simplified Prompt focusing on key instructions and format
        prompt = f"""
Analyze the resume below. Output ONLY the requested information in YAML format.

**Resume:**
```
{resume_text}
```

**Target Skills (use these indexes):**
```
{skill_list_for_prompt}
```

**YAML Output Requirements:**
- Extract `name` (string).
- Extract `email` (string).
- Extract `experience` (list of objects with `title` and `company`).
- Extract `skill_indexes` (list of integers found from the Target Skills list).
- **Add a YAML comment (`#`) explaining the source BEFORE `name`, `email`, `experience`, each item in `experience`, and `skill_indexes`.**

**Example Format:**
```yaml
# Found name at top
name: Jane Doe
# Found email in contact info
email: jane@example.com
# Experience section analysis
experience:
  # First job listed
  - title: Manager
    company: Corp A
  # Second job listed
  - title: Assistant
    company: Corp B
# Skills identified from the target list based on resume content
skill_indexes:
  # Found 0 at top  
  - 0
  # Found 2 in experience
  - 2
```

Generate the YAML output now:
"""
        response = call_llm([{"role": "user", "content": prompt}])

        # --- Minimal YAML Extraction ---
        # Assumes LLM correctly uses ```yaml blocks
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        structured_result = yaml.safe_load(yaml_str)
        # --- End Minimal Extraction ---

        # --- Basic Validation ---
        assert structured_result is not None, "Validation Failed: Parsed YAML is None"
        assert "name" in structured_result, "Validation Failed: Missing 'name'"
        assert "email" in structured_result, "Validation Failed: Missing 'email'"
        assert "experience" in structured_result, "Validation Failed: Missing 'experience'"
        assert isinstance(structured_result.get("experience"), list), "Validation Failed: 'experience' is not a list"
        assert "skill_indexes" in structured_result, "Validation Failed: Missing 'skill_indexes'"
        skill_indexes_val = structured_result.get("skill_indexes")
        assert skill_indexes_val is None or isinstance(skill_indexes_val, list), "Validation Failed: 'skill_indexes' is not a list or None"
        if isinstance(skill_indexes_val, list):
             for index in skill_indexes_val:
                 assert isinstance(index, int), f"Validation Failed: Skill index '{index}' is not an integer"
        # --- End Basic Validation ---

        return structured_result

    def post(self, shared, prep_res, exec_res):
        """Store structured data and print it."""
        shared["structured_data"] = exec_res

        print("\n=== STRUCTURED RESUME DATA (Comments & Skill Index List) ===\n")
        # Dump YAML ensuring block style for readability
        print(yaml.dump(exec_res, sort_keys=False, allow_unicode=True, default_flow_style=None))
        print("\n============================================================\n")
        print("✅ Extracted resume information.")


# === Main Execution Logic ===
if __name__ == "__main__":
    print("=== Resume Parser - Structured Output with Indexes & Comments ===\n")

    # --- Configuration ---
    target_skills_to_find = [
        "Team leadership & management", # 0
        "CRM software",                 # 1
        "Project management",           # 2
        "Public speaking",              # 3
        "Microsoft Office",             # 4
        "Python",                       # 5
        "Data Analysis"                 # 6
    ]
    resume_file = 'data.txt' # Assumes data.txt contains the resume

    # --- Prepare Shared State ---
    shared = {}
    try:
        with open(resume_file, 'r') as file:
            shared["resume_text"] = file.read()
    except FileNotFoundError:
        print(f"Error: Resume file '{resume_file}' not found.")
        exit(1) # Exit if resume file is missing

    shared["target_skills"] = target_skills_to_find

    # --- Define and Run Flow ---
    parser_node = ResumeParserNode(max_retries=3, wait=10)
    flow = Flow(start=parser_node)
    flow.run(shared) # Execute the parsing node

    # --- Display Found Skills ---
    if "structured_data" in shared and "skill_indexes" in shared["structured_data"]:
         print("\n--- Found Target Skills (from Indexes) ---")
         found_indexes = shared["structured_data"]["skill_indexes"]
         if found_indexes: # Check if the list is not empty or None
             for index in found_indexes:
                 if 0 <= index < len(target_skills_to_find):
                     print(f"- {target_skills_to_find[index]} (Index: {index})")
                 else:
                     print(f"- Warning: Found invalid skill index {index}")
         else:
             print("No target skills identified from the list.")
         print("----------------------------------------\n")