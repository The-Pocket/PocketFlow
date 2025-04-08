# Web Search with Analysis

A web search tool built with PocketFlow that performs searches using SerpAPI and analyzes results using LLM.

## Features

- Web search using Google via SerpAPI
- Extracts titles, snippets, and links
- Analyzes search results using GPT-4 to provide:
  - Result summaries
  - Key points/facts
  - Suggested follow-up queries
- Clean command-line interface

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set required API keys:
   ```bash
   export SERPAPI_API_KEY='your-serpapi-key'
   export OPENAI_API_KEY='your-openai-key'
   ```

## Usage

Run the search tool:
```bash
python main.py
```

You will be prompted to:
1. Enter your search query
2. Specify number of results to fetch (default: 5)

The tool will then:
1. Perform the search using SerpAPI
2. Analyze results using GPT-4
3. Present a summary with key points and follow-up queries

## Project Structure

```
pocketflow-tool-search/
├── tools/
│   ├── search.py      # SerpAPI search functionality
│   └── parser.py      # Result analysis using LLM
├── utils/
│   └── call_llm.py    # LLM API wrapper
├── nodes.py           # PocketFlow nodes
├── flow.py           # Flow configuration
├── main.py           # Main script
└── requirements.txt   # Dependencies
```

## Limitations

- Requires SerpAPI subscription
- Rate limited by both APIs
- Basic error handling
- Text results only

## Dependencies

- pocketflow: Flow-based processing
- google-search-results: SerpAPI client
- openai: GPT-4 API access
- pyyaml: YAML processing
