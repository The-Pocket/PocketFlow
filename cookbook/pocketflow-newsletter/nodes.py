from pocketflow import Node
from utils import call_llm, search_web
import yaml

TOPICS = [
    "AI agents framework news this week",
    "LLM benchmark results 2025 2026",
    "AI startup funding rounds this month",
]


class CurateSources(Node):
    """Searches the web for multiple topics to gather raw stories."""

    def prep(self, shared):
        return shared["topics"]

    def exec(self, topics):
        results = []
        for topic in topics:
            print(f"  🔍 Searching: {topic}")
            results.append(search_web(topic))
        return results

    def post(self, shared, prep_res, exec_res):
        shared["raw_stories"] = exec_res
        print(f"  📚 Curated {len(exec_res)} topic searches")


class FilterStories(Node):
    """Picks the 4 most interesting stories from raw search results."""

    def prep(self, shared):
        return shared["raw_stories"]

    def exec(self, stories):
        all_stories = "\n---\n".join(stories)
        prompt = f"""From these raw search results, pick the 4 most interesting stories.
Score on: novelty, impact on practitioners, concrete details (not hype).

Raw results:
{all_stories}

Output ONLY yaml:
```yaml
stories:
  - headline: "..."
    summary: "one sentence"
  - headline: "..."
    summary: "one sentence"
  - headline: "..."
    summary: "one sentence"
  - headline: "..."
    summary: "one sentence"
```"""
        resp = call_llm(prompt)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        return yaml.safe_load(yaml_str)["stories"]

    def post(self, shared, prep_res, exec_res):
        shared["selected"] = exec_res
        print(f"  💡 Selected {len(exec_res)} stories")


class SummarizeStories(Node):
    """Writes punchy newsletter blurbs for each selected story."""

    def prep(self, shared):
        return shared["selected"]

    def exec(self, stories):
        stories_text = "\n\n".join(
            f"Headline: {s['headline']}\nSummary: {s['summary']}"
            for s in stories
        )
        prompt = f"""Write a 2-3 sentence newsletter blurb for each story.
Be punchy, not dry. Include why it matters.

{stories_text}

Output ONLY yaml:
```yaml
blurbs:
  - headline: "..."
    blurb: "..."
  - headline: "..."
    blurb: "..."
  - headline: "..."
    blurb: "..."
  - headline: "..."
    blurb: "..."
```"""
        resp = call_llm(prompt)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        return yaml.safe_load(yaml_str)["blurbs"]

    def post(self, shared, prep_res, exec_res):
        for story, blurb_entry in zip(shared["selected"], exec_res):
            story["blurb"] = blurb_entry["blurb"]
        print(f"  ✍️ Summarized {len(exec_res)} stories")


class FormatNewsletter(Node):
    """Creates a formatted markdown newsletter from the blurbed stories."""

    def prep(self, shared):
        return shared["selected"]

    def exec(self, stories):
        sections = []
        for i, s in enumerate(stories, 1):
            sections.append(f"## {i}. {s['headline']}\n{s['blurb']}")
        body = "\n\n".join(sections)
        return f"# AI Weekly Digest\n\n{body}"

    def post(self, shared, prep_res, exec_res):
        shared["newsletter"] = exec_res
        print("  ✅ Newsletter formatted")
