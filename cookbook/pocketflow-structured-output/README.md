# Structured Output Demo

A minimal demo application showing how to use PocketFlow to extract structured data from a resume using direct prompting and YAML formatting.

## Features

- Extracts structured data using prompt engineering
- Validates output structure before processing

## Run It

1. Make sure your OpenAI API key is set:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```
    Alternatively, you can edit the `utils.py` file to include your API key directly.

2. Edit data.txt with the resume you want to parse (a sample resume is already included)

3. Install requirements and run the application:
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

## How It Works

```mermaid
flowchart LR
    parser[ResumeParserNode]
```

The Resume Parser application uses a single node that:
1. Takes resume text from the shared state (loaded from data.txt)
2. Sends the resume to an LLM with a prompt that requests YAML formatted output
3. Extracts and validates the structured YAML data
4. Outputs the structured result

## Files

- [`main.py`](./main.py): Implementation of the ResumeParserNode
- [`utils.py`](./utils.py): LLM utilities
- [`data.txt`](./data.txt): Sample resume text file
 
## Example Output

```
=== STRUCTURED RESUME DATA ===

name: John Smith
email: johnsmtih1983@gnail.com
experience:
- title: Sales Manager
  company: ABC Corporation
- title: Assistant Manager
  company: XYZ Industries
- title: Customer Service Representative
  company: Fast Solutions Inc
skills:
- Microsoft Office: Excel, Word, PowerPoint (Advanced)
- Customer relationship management (CRM) software
- Team leadership & management
- Project management
- Public speaking
- Time management

============================
```