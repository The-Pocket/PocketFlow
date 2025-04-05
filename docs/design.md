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
        AnalyzeLinkedIn --> GenerateEmail(Generate Email - AI)

        CheckLinkedIn -- "no_linkedin" --> GenerateEmail

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

7.  **`AnalyzeLinkedIn`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads `shared["linkedin_raw_profile"]`.
    *   `exec(prep_res)`: Calls `utils.ai_analyzer.analyze_linkedin_profile(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Writes the analysis result (dictionary or error dict) to `shared["linkedin_report"] = exec_res`.
    *   `returns`: `"default"` -> `GenerateEmail`

8.  **`GenerateEmail`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads the required context from `shared` (e.g., `shared['lead_name']`, `shared['company_name']`, `shared.get('website_report')`, `shared.get('linkedin_report')`). Packages this into a dictionary.
    *   `exec(prep_res)`: Calls `utils.ai_generator.generate_email_draft(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Writes the generated email subject and body from `exec_res` (e.g., `exec_res['subject']`, `exec_res['body']`) to `shared["email_subject"]` and `shared["email_body"]`.
    *   `returns`: `"default"` -> `StoreResults`

9.  **`StoreResults`** (Node)
    *   `type`: Regular
    *   `prep(shared)`: Reads all relevant data points we want to save from `shared` (initial lead info, reports, email subject/body) and structures them into a final dictionary for Supabase.
    *   `exec(prep_res)`: Calls `utils.database.save_to_supabase(prep_res)`.
    *   `post(shared, prep_res, exec_res)`: Logs the result (`exec_res` which is True/False).
    *   `returns`: `"default"` (ends flow).

### Shared Store Structure (V1)

```python
shared = {
    # Initial Input (from LoadLeadData)
    "lead_name": "...",
    "last_name": "...", # Optional
    "company_name": "...",
    "company_website": "...", # Optional
    "linkedin_url": "...", # Optional

    # Intermediate Results
    "website_raw_content": "...", # From ScrapeWebsite (or None/Error)
    "website_report": { ... },     # From AnalyzeWebsite (or None/Error)
    "linkedin_raw_profile": { ... },# From ScrapeLinkedIn (or None/Error)
    "linkedin_report": { ... },    # From AnalyzeLinkedIn (or None/Error)

    # Final Output
    "email_subject": "...",      # From GenerateEmail
    "email_body": "..."          # From GenerateEmail
}
``` 