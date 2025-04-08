# PocketFlow Tool: PDF Vision

A PocketFlow example project demonstrating PDF processing with OpenAI's Vision API for OCR and text extraction.

## Features

- Convert PDF pages to images while maintaining quality and size limits
- Extract text from scanned documents using GPT-4 Vision API
- Support for custom extraction prompts
- Maintain page order and formatting in extracted text
- Batch processing of multiple PDFs from a directory

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Place your PDF files in the `pdfs` directory
2. Run the example:
   ```bash
   python main.py
   ```
   The script will process all PDF files in the `pdfs` directory and output the extracted text for each one.

## Project Structure

```
pocketflow-tool-pdf-vision/
├── pdfs/           # Directory for PDF files to process
├── tools/
│   ├── pdf.py     # PDF to image conversion
│   └── vision.py  # Vision API integration
├── utils/
│   └── call_llm.py # OpenAI client config
├── nodes.py       # PocketFlow nodes
├── flow.py        # Flow configuration
└── main.py        # Example usage
```

## Flow Description

1. **LoadPDFNode**: Loads PDF and converts pages to images
2. **ExtractTextNode**: Processes images with Vision API
3. **CombineResultsNode**: Combines extracted text from all pages

## Customization

You can customize the extraction by modifying the prompt in `shared`:

```python
shared = {
    "pdf_path": "your_file.pdf",
    "extraction_prompt": "Your custom prompt here"
}
```

## Limitations

- Maximum PDF page size: 2000px (configurable in `tools/pdf.py`)
- Vision API token limit: 1000 tokens per response
- Image size limit: 20MB per image for Vision API

## License

MIT
