import os
import tempfile
import subprocess
from pocketflow import Node
from utils import call_llm

class WriteChart(Node):
    """Generates a Mermaid diagram from a description, incorporating error feedback from previous attempts."""

    def prep(self, shared):
        shared.setdefault("attempts", [])
        return {"task": shared["task"], "attempts": shared["attempts"]}

    def exec(self, inputs):
        print("✍️  Generating Mermaid diagram...")

        # Build history of previous failed attempts
        history = "\n\n".join(
            f"Attempt {i+1}:\n```mermaid\n{a['code']}\n```\nError: {a['error']}"
            for i, a in enumerate(inputs["attempts"])
        )

        prompt = f"""Write a Mermaid diagram for: {inputs['task']}

Output ONLY the mermaid code in a ```mermaid``` block. Do not include any other text."""

        if history:
            prompt += f"""

Previous failed attempts and their errors:
{history}

Fix the syntax errors from the previous attempts. Make sure the diagram compiles correctly."""

        response = call_llm(prompt)
        code = response.split("```mermaid")[1].split("```")[0].strip()
        return code

    def post(self, shared, prep_res, exec_res):
        shared["chart"] = exec_res
        print(f"  Generated chart ({len(exec_res)} chars)")


class CompileChart(Node):
    """Compiles a Mermaid diagram using mermaid-cli (npx mmdc). Returns success/failure with error details."""

    def prep(self, shared):
        return shared["chart"]

    def exec(self, code):
        print("🔍 Compiling Mermaid diagram...")

        # Write mermaid code to a temp file
        with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as f:
            f.write(code)
            mmd_path = f.name

        svg_path = mmd_path.replace(".mmd", ".svg")

        try:
            result = subprocess.run(
                ["npx", "--yes", "@mermaid-js/mermaid-cli", "-i", mmd_path, "-o", svg_path],
                capture_output=True,
                text=True,
                timeout=60
            )
        except subprocess.TimeoutExpired:
            os.unlink(mmd_path)
            return {"success": False, "error": "Compilation timed out after 60 seconds"}

        # Clean up temp files
        os.unlink(mmd_path)
        svg_exists = os.path.exists(svg_path)
        if svg_exists:
            os.unlink(svg_path)

        if result.returncode != 0 or not svg_exists:
            error = result.stderr or result.stdout
            # Extract the most relevant error lines
            lines = error.split("\n")
            clean = [l for l in lines if "Parse error" in l or "Expecting" in l or "Error" in l]
            clean_error = "\n".join(clean[:3]) if clean else error[:500]
            return {"success": False, "error": clean_error}

        return {"success": True}

    def post(self, shared, prep_res, exec_res):
        if exec_res["success"]:
            print("  Compiled successfully! ✅")
            return "done"

        attempt_num = len(shared["attempts"]) + 1
        print(f"  Compilation failed (attempt {attempt_num}/3)")
        print(f"  Error: {exec_res['error'][:200]}")

        shared["attempts"].append({
            "code": shared["chart"],
            "error": exec_res["error"]
        })

        if len(shared["attempts"]) >= 3:
            print("  Max retries reached. Giving up.")
            return "done"

        print("  💡 Will retry with error feedback...")
        return "fix"
