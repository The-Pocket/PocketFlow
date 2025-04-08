"""Generates prompts for third-party data analysis and query generation."""

from datetime import date

def generate_tavily_query_prompt(lead_first_name: str, lead_last_name: str, company_name: str) -> str:
    """Generates a prompt to create search queries for Tavily."""
    # Ensure names are handled even if empty
    lead_full_name = f"{lead_first_name} {lead_last_name}".strip()
    lead_str = lead_full_name if lead_full_name else "the lead"
    company_str = f"at {company_name}" if company_name else ""
    target_company = company_name if company_name else 'the company'
    target_lead = lead_full_name if lead_full_name else 'the lead' # Use full name for search terms
    
    return f"""
You are an expert sales researcher. Generate 3-5 specific, actionable search queries to find valuable information about {lead_full_name} {company_str} that would help in sales outreach. Focus *only* on third-party sources (news, reviews, forums, conference sites, etc.), avoiding the company's own website or LinkedIn.

GOALS:
- Find company challenges, recent news (partnerships, funding, acquisitions), tech stack mentions, or relevant industry trends.
- Discover the prospect's external presence (conference talks, podcast interviews, articles authored).
- Uncover customer sentiment from review sites or forums.
- Find unique insights not easily found on LinkedIn or the company website.

SEARCH STRATEGIES TO CONSIDER:
- Site-specific searches: `\"{target_company}\" review site:trustpilot.com`, `\"{target_company}\" site:g2.com`, `\"{target_company}\" site:capterra.com`
- Prospect activities: `\"{target_lead}\" speaker conference`, `\"{target_lead}\" podcast guest`, `\"{target_lead}\" author article`
- Company news/analysis: `\"{target_company}\" mentioned in report`, `\"{target_company}\" analysis`, `\"{target_company}\" funding`, `\"{target_company}\" acquisition`
- Community discussions: `\"{target_company}\" reddit`, `\"{target_company}\" forum discussion`
- Industry context: `\"[Industry term] regulation affecting {target_company}\"`, `\"{target_company}\" industry trends`

OUTPUT REQUIREMENTS:
- Generate 5 queries.
- Queries should be specific (e.g., `\"Acme Corp funding announcement 2024\"` instead of `\"Acme Corp news\"`).
- Return your response as a JSON list of strings only, with no other text before or after.

Example JSON Output Format:
```json
[
  "query 1",
  "query 2",
  "query 3"
]
```
"""

def generate_analysis_prompt(lead_first_name: str, lead_last_name: str, company_name: str, sources: list, current_date: date) -> str:
    """Generates a prompt to analyze third-party source data based on provided sources."""
    source_text = ""
    if not sources:
        source_text = "No third-party sources provided.\n"
    else:
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Untitled')
            snippet = source.get('snippet', 'No Snippet Available')
            url = source.get('url', 'No URL')
            source_text += f"Source {i}:\nTitle: {title}\nURL: {url}\nSnippet: {snippet}\n\n"

    # Ensure names are handled even if empty
    lead_full_name = f"{lead_first_name} {lead_last_name}".strip()
    lead_str = lead_full_name if lead_full_name else "the lead"
    company_str = f"at {company_name}" if company_name else "for the target company"

    return f"""
You are a precision lead intelligence agent tasked with finding specific, actionable insights about {lead_str} {company_str} based *only* on the third-party information provided below.
Your goal is to discover unique information that automated scraping of LinkedIn or the company's main website would miss. You will be evaluated on the uniqueness and actionability of your findings.

Current Date: {current_date.strftime('%Y-%m-%d')}

PROVIDED THIRD-PARTY SOURCES:
--- START SOURCES ---
{source_text}
--- END SOURCES ---

ANALYSIS TASK:
Review ONLY the sources provided above. Generate a concise intelligence report focusing *exclusively* on information derivable from these sources. Do NOT use external knowledge or make assumptions. If information for a section isn't present in the sources, explicitly state that.

OUTPUT FORMAT:
Structure your report exactly as follows, citing the source number(s) (e.g., [Source 1], [Source 2, 3]) for every piece of information:

1.  INDUSTRY CONTEXT (1-2 bullet points MAX):
    *   [Market positioning, competitive analysis, regulatory/trend impacts derived *only* from the provided sources. Cite source(s).]
    *   [Another distinct point if available. Cite source(s).]
    *   *(If no relevant info found in sources, state: "No specific industry context found in provided sources.")*

2.  CUSTOMER SENTIMENT (1-2 bullet points MAX):
    *   [Specific praise or criticism mentioned in the sources (e.g., from reviews, forums). Quote directly if possible. Cite source(s).]
    *   [Another distinct point if available. Cite source(s).]
    *   *(If no relevant info found in sources, state: "No specific customer sentiment found in provided sources.")*

3.  UNIQUE CONVERSATION ANGLE (1 specific insight MAX):
    *   [Identify one surprising, non-obvious, or specific piece of information (e.g., prospect's recent talk, specific company challenge mentioned) that could be used to personalize outreach. Must be derived *only* from the sources. Cite source(s).]
    *   *(If no unique angle found, state: "No unique conversation angle identified in provided sources.")*

IMPORTANT CONSTRAINTS:
- Base your entire report ONLY on the text within the 'PROVIDED THIRD-PARTY SOURCES' section.
- Do NOT include any information commonly found on LinkedIn profiles (e.g., job titles, work history) or the company's own website (e.g., product marketing descriptions), unless it's uniquely presented or contextualized in the provided sources.
- Prioritize quality over quantity. A single, unique, well-sourced insight is more valuable than generic points.
- Cite the source number(s) for every claim.
""" 