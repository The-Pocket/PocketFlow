from pathlib import Path
import os
from openai import OpenAI


def load_skills(skills_dir: str) -> dict[str, str]:
    skills = {}
    for md_file in sorted(Path(skills_dir).glob("*.md")):
        skills[md_file.stem] = md_file.read_text(encoding="utf-8")

    if not skills:
        raise ValueError(f"No skill files found in {skills_dir}")
    return skills


def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
