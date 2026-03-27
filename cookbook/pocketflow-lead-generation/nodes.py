from pocketflow import Node
from utils import call_llm, PRODUCT, SAMPLE_LEADS
import yaml


class ScrapeLeads(Node):
    def prep(self, shared):
        """Load leads from shared store or use sample data."""
        return shared.get("leads", SAMPLE_LEADS)

    def exec(self, leads):
        """Return leads as-is (sample data, no scraping needed)."""
        return leads

    def post(self, shared, prep_res, exec_res):
        shared["leads"] = exec_res
        print(f"  📋 Loaded {len(exec_res)} leads")


class EnrichLeads(Node):
    def prep(self, shared):
        """Read leads for enrichment."""
        return shared["leads"]

    def exec(self, leads):
        """Enrich leads with company info (simulated — data already in sample)."""
        return leads

    def post(self, shared, prep_res, exec_res):
        shared["leads"] = exec_res
        print(f"  🔍 Enriched {len(exec_res)} leads with company intel")


class ScoreLeads(Node):
    def prep(self, shared):
        """Read leads for scoring."""
        return shared["leads"]

    def exec(self, leads):
        """Use LLM to score each lead 1-10 on fit for the product."""
        leads_text = "\n".join(
            f"- {l['name']}, {l['title']} at {l['company']}: {l.get('enrichment', '')}"
            for l in leads
        )
        prompt = f"""Score each lead 1-10 for selling "{PRODUCT}".
Score based on: likely need for LLM tooling, seniority, technical role.

Leads:
{leads_text}

Output ONLY yaml:
```yaml
scores:
  - name: "Sarah Chen"
    score: 8
    reason: "one sentence why"
```"""
        resp = call_llm(prompt)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        return yaml.safe_load(yaml_str)["scores"]

    def post(self, shared, prep_res, exec_res):
        score_map = {s["name"]: s for s in exec_res}
        for lead in shared["leads"]:
            match = score_map.get(lead["name"], {})
            lead["score"] = match.get("score", 0)
            lead["score_reason"] = match.get("reason", "")
        shared["leads"].sort(key=lambda x: x["score"], reverse=True)
        for lead in shared["leads"]:
            emoji = "🟢" if lead["score"] >= 6 else "🔴"
            print(f"  {emoji} {lead['name']} ({lead['title']}): {lead['score']}/10 — {lead['score_reason']}")


class PersonalizeEmails(Node):
    def prep(self, shared):
        """Filter to hot leads (score >= 6)."""
        hot = [l for l in shared["leads"] if l["score"] >= 6]
        print(f"  ✍️  Generating personalized emails for {len(hot)} qualified leads...")
        return hot

    def exec(self, hot_leads):
        """Generate a personalized cold email for each hot lead."""
        emails = []
        for lead in hot_leads:
            prompt = f"""Write a 3-sentence cold email to {lead['name']}, {lead['title']} at {lead['company']}.
Product: {PRODUCT}
About them: {lead.get('enrichment', '')}

Rules:
- Reference something specific about their company
- Connect to a problem they likely have
- End with a specific ask (15 min call)
- No filler phrases
- Subject line first"""
            emails.append({"lead": lead, "email": call_llm(prompt)})
        return emails

    def post(self, shared, prep_res, exec_res):
        shared["emails"] = exec_res
        print(f"  ✅ Generated {len(exec_res)} personalized emails")
