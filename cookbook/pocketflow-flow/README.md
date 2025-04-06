# Text Converter Flow

This project demonstrates an interactive text transformation tool built with PocketFlow.

## Features

- Convert text to UPPERCASE
- Convert text to lowercase
- Reverse text
- Remove extra spaces
- Interactive command-line interface
- Continuous flow with option to process multiple texts

## Getting Started

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python main.py
```

## How It Works

The workflow features an interactive loop with branching paths:

```mermaid
graph TD
    Input[TextInput Node] -->|transform| Transform[TextTransform Node]
    Transform -->|input| Input
    Transform -->|exit| End[End]
    Input -->|exit| End
```

Here's what each part does:
1. **TextInput Node**: Collects text input and handles menu choices
2. **TextTransform Node**: Applies the selected transformation to the text

## Example Output

```
Welcome to Text Converter!
=========================

Enter text to convert: Pocket Flow is a 100-line LLM framework

Choose transformation:
1. Convert to UPPERCASE
2. Convert to lowercase
3. Reverse text
4. Remove extra spaces
5. Exit

Your choice (1-5): 1

Result: POCKET FLOW IS A 100-LINE LLM FRAMEWORK

Convert another text? (y/n): n

Thank you for using Text Converter!
```

## Files

- [`main.py`](./main.py): Main entry point for running the text converter
- [`flow.py`](./flow.py): Defines the nodes and flow for text transformation
- [`requirements.txt`](./requirements.txt): Lists the required dependencies
