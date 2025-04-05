# Project: Personalized Email Generation SaaS

## 1. Requirements (V1)

*   **Problem:** Automate the research and drafting of personalized outreach emails for leads.
*   **Goal:** Increase efficiency and effectiveness of sales/marketing outreach.
*   **Input:** CSV via Flask interface containing optional `name`, `last_name`, `company_name`, `company_website`, `linkedin_url`.
*   **Core Features (V1):**
    *   Analyze company website content (if URL provided).
    *   Analyze lead's LinkedIn profile (if URL provided).
    *   Generate one personalized email draft (Subject & Body) based on available input and analysis.
    *   Store input data, analysis reports, and generated email in Supabase.
*   **AI Fit:** Leverages LLMs for text analysis, synthesis, and generation.

## 2. Flow Design (V1)

*   **Pattern:** Workflow
*   **Description:** Processes one lead at a time. Checks for website URL, scrapes/analyzes if present. Checks for LinkedIn URL, scrapes/analyzes if present. Synthesizes available information to generate an email. Stores results.
*   **Diagram:**
    ```mermaid
    flowchart TD
        Start(LoadLeadData) --> CheckWebsite{Has Website?}

        CheckWebsite -- "has_website" --> ScrapeWebsite(Scrape Website - Firecrawl)
        ScrapeWebsite --> AnalyzeWebsite(Analyze Website - AI)
        AnalyzeWebsite --> CheckLinkedIn{Has LinkedIn?}

        CheckWebsite -- "no_website" --> CheckLinkedIn

        CheckLinkedIn -- "has_linkedin" --> ScrapeLinkedIn(Scrape LinkedIn - Apify)
        ScrapeLinkedIn --> AnalyzeLinkedIn(Analyze LinkedIn - AI)
        AnalyzeLinkedIn --> SearchTavily(Search Third-Party - Tavily)

        CheckLinkedIn -- "no_linkedin" --> SearchTavily

        SearchTavily --> AnalyzeTavily(Analyze Third-Party - AI)
        AnalyzeTavily --> GenerateEmail(Generate Email - AI)

        GenerateEmail --> StoreResults(Store Results - Supabase)
        StoreResults --> End(End)
    ```

## 3. Utilities (V1)

Here are the utility functions needed for V1:

1.  **`call_firecrawl(url: str) -> str`** (`utils/web_scraper.py`)
    *   **Input:** Company website URL.
    *   **Output:** Scraped website text content as a string.
    *   **Necessity:** Used by `ScrapeWebsite` node to fetch website data for analysis. Requires Firecrawl API key/setup.
    *   *(Initial Implementation: Can return placeholder text)*

2.  **`analyze_website_content(website_text: str) -> dict`** (`utils/ai_analyzer.py`)
    *   **Input:** Raw website text.
    *   **Output:** Dictionary containing structured analysis (e.g., `{"products": [...], "audience": "...", "value_prop": "..."}`).
    *   **Necessity:** Used by `AnalyzeWebsite` node. Requires LLM API call with a specific prompt for website content.
    *   *(Initial Implementation: Can return a fixed dictionary)*

3.  **`call_apify_linkedin_profile(url: str) -> dict`** (`utils/linkedin_scraper.py`)
    *   **Input:** Lead's LinkedIn profile URL.
    *   **Output:** Dictionary containing scraped profile data (e.g., job history, skills, summary).
    *   **Necessity:** Used by `ScrapeLinkedIn` node. Requires Apify API key and actor setup.
    *   *(Initial Implementation: Can return placeholder profile data)*

4.  **`analyze_linkedin_profile(profile_data: dict) -> dict`** (`utils/ai_analyzer.py`)
    *   **Input:** Dictionary of scraped LinkedIn profile data.
    *   **Output:** Dictionary containing structured analysis (e.g., `{"career_summary": "...", "key_skills": [...], "focus_areas": [...]}`).
    *   **Necessity:** Used by `AnalyzeLinkedIn` node. Requires LLM API call with a specific prompt for LinkedIn profiles.
    *   *(Initial Implementation: Can return a fixed dictionary)*

5.  **`generate_email_draft(context: dict) -> dict`** (`utils/ai_generator.py`)
    *   **Input:** Dictionary containing all available lead info and analysis reports (`lead_name`, `company_name`, `website_report`, `linkedin_report`, etc.).
    *   **Output:** Dictionary containing the generated email (e.g., `{"subject": "...", "body": "..."}`).
    *   **Necessity:** Used by `GenerateEmail` node. Requires LLM API call with a synthesis/generation prompt.
    *   *(Initial Implementation: Can return a fixed email string)*

6.  **`save_to_supabase(lead_data: dict) -> bool`** (`utils/database.py`)
    *   **Input:** Dictionary containing the complete lead record (initial info + reports + email).
    *   **Output:** Boolean indicating success/failure.
    *   **Necessity:** Used by `StoreResults` node to persist data. Requires Supabase credentials and table setup.
    *   *(Initial Implementation: Can simply print the data)*

7.  **`call_tavily_search(query: str, max_results: int = 3) -> list[dict]`** (`utils/search.py`)
    *   **Input:** Search query string.
    *   **Output:** List of Tavily search result dictionaries `[{'title': ..., 'url': ..., 'content': ...}]`.
    *   **Necessity:** Used by `SearchThirdPartySources` node to query external sources. Requires `TAVILY_API_KEY` environment variable.

### 3.1 Database Schema (Supabase V1)

The following SQL statement defines the structure for the `leads` table in Supabase, used by the `save_to_supabase` utility.

```sql
CREATE TABLE public.leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Unique ID for each record
  lead_name TEXT,
  last_name TEXT,
  company_name TEXT,
  company_website TEXT,
  linkedin_url TEXT UNIQUE, -- Make LinkedIn URL unique if present
  website_analysis_report JSONB, -- Store JSON analysis results
  linkedin_analysis_report JSONB, -- Store JSON analysis results
  generated_email_subject TEXT,
  generated_email_body TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
  -- Add other columns as needed, e.g., status, score, owner_id etc.
);

-- Optional: Comment explaining the table purpose
COMMENT ON TABLE public.leads IS 'Stores processed lead information and generated email content.';

-- Optional: Enable Row Level Security (Good Practice!)
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
-- Define policies later based on your access patterns

-- Optional: Function and Trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_leads_update
BEFORE UPDATE ON public.leads
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();
```

## 4. Node Design (V1)

Details on how each node interacts with the shared store and utilities.

1.  **`LoadLeadData`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads initial lead parameters (passed into the flow's `run` method, e.g., `{"lead_name": "...", "company_name": ...}`).
    *   `exec(prep_res)`: Simply passes the input data through.
    *   `post(shared, prep_res, exec_res)`: Copies the input lead data (`exec_res`) into the main `shared` store (e.g., `shared.update(exec_res)`). Initializes empty placeholders in `shared` for reports and email (e.g., `shared['website_report'] = None`, `shared['linkedin_report'] = None`, `shared['email_subject'] = None`, `shared['email_body'] = None`).
    *   `returns`: `"default"` -> `CheckWebsiteExists`

2.  **`CheckWebsiteExists`** (Node)
    *   `type`: Regular (Decision Node)
    *   `prep(shared)`: Reads `shared.get("company_website")`.
    *   `exec(prep_res)`: Checks if `prep_res` (the website URL) is a non-empty string and looks like a plausible URL (basic check).
    *   `post(shared, prep_res, exec_res)`: No changes to `shared`.
    *   `returns`: `"has_website"` if `exec_res` is True, else `"no_website"`.

3.  **`ScrapeWebsite`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `shared["company_website"]`.
    *   `exec(prep_res)`: Calls `utils.web_scraper.call_firecrawl(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Writes the result (scraped text or error message) to `shared["website_raw_content"] = exec_res`.
    *   `returns`: `"default"` -> `AnalyzeWebsite`

4.  **`AnalyzeWebsite`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `shared["website_raw_content"]`.
    *   `exec(prep_res)`: Calls `utils.ai_analyzer.analyze_website_content(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Writes the analysis result (dictionary or error dict) to `shared["website_report"] = exec_res`.
    *   `returns`: `"default"` -> `CheckLinkedInExists`

5.  **`CheckLinkedInExists`** (Node)
    *   `type`: Regular (Decision Node)
    *   `prep(shared)`: Reads `shared.get("linkedin_url")`.
    *   `exec(prep_res)`: Checks if `prep_res` (the LinkedIn URL) is a non-empty string and looks like a plausible LinkedIn URL.
    *   `post(shared, prep_res, exec_res)`: No changes to `shared`.
    *   `returns`: `"has_linkedin"` if `exec_res` is True, else `"no_linkedin"`.

6.  **`ScrapeLinkedIn`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `shared["linkedin_url"]`.
    *   `exec(prep_res)`: Calls `utils.linkedin_scraper.call_apify_linkedin_profile(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Writes the result (profile data dict or error dict) to `shared["linkedin_raw_profile"] = exec_res`.
    *   `returns`: `"default"` -> `AnalyzeLinkedIn`

7.  **`SearchThirdPartySources`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `company_name`, `lead_name`, `last_name`. Generates targeted search queries for Tavily based on predefined strategies (reviews, news, publications, etc.).
    *   `exec(prep_res)`: Takes list of queries. Calls `utils.search.call_tavily_search` for a limited number of queries, collecting and deduplicating results.
    *   `post(shared, prep_res, exec_res)`: Stores the list of unique search result dictionaries in `shared['third_party_search_results']`.
    *   `returns`: `"default"` -> `AnalyzeThirdPartySources`

8.  **`AnalyzeThirdPartySources`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `shared['third_party_search_results']`. Formats results into a string for the LLM prompt.
    *   `exec(prep_res)`: Takes formatted results. Calls `utils.ai_analyzer.call_llm_with_json_output` using the detailed "Precision Lead Intelligence Agent" prompt (requesting JSON output with `industry_context`, `customer_sentiment`, `unique_conversation_angle`).
    *   `post(shared, prep_res, exec_res)`: Stores the structured JSON analysis result in `shared['precision_intelligence_report']`.
    *   `returns`: `"default"` -> `GenerateEmail`

9.  **`GenerateEmail`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `lead_name`, `company_name`, `website_report`, `linkedin_report`, and `precision_intelligence_report`. Packages into a context dictionary.
    *   `exec(prep_res)`: Calls `utils.ai_generator.generate_email_draft` with the context. The underlying prompt prioritizes using the `precision_intelligence_report` for personalization.
    *   `post(shared, prep_res, exec_res)`: Stores `exec_res['subject']` and `exec_res['body']` into `shared`.
    *   `returns`: `"default"` -> `StoreResults`

10. **`StoreResults`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Now also includes `precision_intelligence_report` when preparing `data_to_save`.
    *   `exec(prep_res)`: Calls `utils.database.save_to_supabase`.
    *   `post(shared, prep_res, exec_res)`: Logs result.
    *   `returns`: `"default"` (ends flow).

### Shared Store Structure (V1 Updated)

```python
shared = {
    # Initial Input
    "lead_name": "...",
    "last_name": "...",
    "company_name": "...",
    "company_website": "...",
    "linkedin_url": "...",

    # Intermediate Results
    "website_raw_content": "...", 
    "website_report": { ... },
    "linkedin_raw_profile": { ... },
    "linkedin_report": { ... },
    "third_party_search_results": [ ... ], # List of Tavily results
    "precision_intelligence_report": { ... }, # Structured analysis from Tavily results

    # Final Output
    "email_subject": "...",
    "email_body": "..."
}
``` 