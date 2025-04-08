# Web Crawler with Content Analysis

A web crawler tool built with PocketFlow that crawls websites and analyzes content using LLM.

## Features

- Crawls websites while respecting domain boundaries
- Extracts text content and links from pages
- Analyzes content using GPT-4 to generate:
  - Page summaries
  - Main topics/keywords
  - Content type classification
- Processes pages in batches for efficiency
- Generates a comprehensive analysis report

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

## Usage

Run the crawler:
```bash
python main.py
```

You will be prompted to:
1. Enter the website URL to crawl
2. Specify maximum number of pages to crawl (default: 10)

The tool will then:
1. Crawl the specified website
2. Extract and analyze content using GPT-4
3. Generate a report with findings

## Project Structure

```
pocketflow-tool-crawler/
├── tools/
│   ├── crawler.py     # Web crawling functionality
│   └── parser.py      # Content analysis using LLM
├── utils/
│   └── call_llm.py    # LLM API wrapper
├── nodes.py           # PocketFlow nodes
├── flow.py           # Flow configuration
├── main.py           # Main script
└── requirements.txt   # Dependencies
```

## Limitations

- Only crawls within the same domain
- Text content only (no images/media)
- Rate limited by OpenAI API
- Basic error handling

## Dependencies

- pocketflow: Flow-based processing
- requests: HTTP requests
- beautifulsoup4: HTML parsing
- openai: GPT-4 API access
