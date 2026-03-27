from pocketflow import Flow
from nodes import ScrapeLeads, EnrichLeads, ScoreLeads, PersonalizeEmails


def create_lead_generation_flow():
    """
    Create a linear sales pipeline flow.

    Pipeline:
    1. ScrapeLeads   — load sample lead data
    2. EnrichLeads   — enrich with company intel (simulated)
    3. ScoreLeads    — LLM scores each lead 1-10
    4. PersonalizeEmails — generate cold emails for hot leads

    Returns:
        Flow: A complete lead-generation pipeline flow
    """
    scrape = ScrapeLeads()
    enrich = EnrichLeads()
    score = ScoreLeads()
    personalize = PersonalizeEmails()

    # Linear chain
    scrape >> enrich >> score >> personalize

    return Flow(start=scrape)
