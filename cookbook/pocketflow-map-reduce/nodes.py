from pocketflow import Node, BatchNode
from utils import call_llm
import yaml
import os

class ReadResumesNode(Node):
    """Map phase: Read all resumes from the data directory into shared storage."""
    
    def exec(self, _):
        resume_files = {}
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    resume_files[filename] = file.read()
        
        return resume_files
    
    def post(self, shared, prep_res, exec_res):
        shared["resumes"] = exec_res
        return "default"


class EvaluateResumesNode(BatchNode):
    """Batch processing: Evaluate each resume to determine if the candidate qualifies."""
    
    def prep(self, shared):
        return list(shared["resumes"].items())
    
    def exec(self, resume_item):
        """Evaluate a single resume."""
        filename, content = resume_item
        
        prompt = f"""
Evaluate the following resume and determine if the candidate qualifies for an advanced technical role.
Criteria for qualification:
- At least a bachelor's degree in a relevant field
- At least 3 years of relevant work experience
- Strong technical skills relevant to the position

Resume:
{content}

Return your evaluation in YAML format:
```yaml
candidate_name: [Name of the candidate]
qualifies: [true/false]
reasons:
  - [First reason for qualification/disqualification]
  - [Second reason, if applicable]
```
"""
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response
        result = yaml.safe_load(yaml_content)
        
        return (filename, result)

    def post(self, shared, prep_res, exec_res_list):
        shared["evaluations"] = {filename: result for filename, result in exec_res_list}
        return "default"


class ReduceResultsNode(Node):
    """Reduce node: Count and print out how many candidates qualify."""
    
    def prep(self, shared):
        return shared["evaluations"]
    
    def exec(self, evaluations):
        qualified_count = 0
        total_count = len(evaluations)
        qualified_candidates = []
        
        for filename, evaluation in evaluations.items():
            if evaluation.get("qualifies", False):
                qualified_count += 1
                qualified_candidates.append(evaluation.get("candidate_name", "Unknown"))
        
        summary = {
            "total_candidates": total_count,
            "qualified_count": qualified_count,
            "qualified_percentage": round(qualified_count / total_count * 100, 1) if total_count > 0 else 0,
            "qualified_names": qualified_candidates
        }
        
        return summary
    
    def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
        
        print("\n===== Resume Qualification Summary =====")
        print(f"Total candidates evaluated: {exec_res['total_candidates']}")
        print(f"Qualified candidates: {exec_res['qualified_count']} ({exec_res['qualified_percentage']}%)")
        
        if exec_res['qualified_names']:
            print("\nQualified candidates:")
            for name in exec_res['qualified_names']:
                print(f"- {name}")
        
        return "default" 